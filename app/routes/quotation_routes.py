from flask import Blueprint, request, jsonify
from app import db
from app.models.quotation import Quotation, QuotationItem
from datetime import datetime, date
from sqlalchemy import func, extract
from sqlalchemy.exc import IntegrityError

quotations_bp = Blueprint('quotations', __name__)

# ================= COMPANY INFO (Default) =================
DEFAULT_COMPANY_INFO = {
    'name': "SRI RAJA MOSQUITO NETLON SERVICES",
    'description': "Manufacture & Dealer in Mosquito & Insect Net (WholeSale & Retail)",
    'phone': "+91 9790569529",
    'gstin': "33BECPR927M1ZU",
    'address': "Ryan Complex Vadavalli Road, Edayarpalayam, Coimbatore-25",
    'branch': "Edayarpalayam",
}

# ================= HELPER FUNCTIONS =================
def generate_quotation_number():
    year = datetime.now().year
    last_quote = Quotation.query.filter(
        Quotation.quotation_no.like(f'QT-{year}-%')
    ).order_by(Quotation.id.desc()).first()

    if last_quote and last_quote.quotation_no:
        try:
            last_num = int(last_quote.quotation_no.split('-')[-1])
            new_num = last_num + 1
        except:
            new_num = 1
    else:
        new_num = 1

    return f"QT-{year}-{new_num:04d}"


def validate_quotation_data(data):
    errors = []

    if not data.get('customerInfo', {}).get('billTo'):
        errors.append("Customer name is required")
    if not data.get('customerInfo', {}).get('contactNo'):
        errors.append("Contact number is required")

    items = data.get('items', [])
    if not items:
        errors.append("At least one item is required")

    return errors


# ================= GET ALL QUOTATIONS =================
@quotations_bp.route('/quotations', methods=['GET'])
def get_quotations():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        pagination = Quotation.query.order_by(
            Quotation.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)

        total_value = db.session.query(
            func.sum(Quotation.grand_total)
        ).scalar() or 0

        this_month = datetime.now().month
        this_year = datetime.now().year

        this_month_count = Quotation.query.filter(
            extract('month', Quotation.created_at) == this_month,
            extract('year', Quotation.created_at) == this_year
        ).count()

        return jsonify({
            "quotations": [q.to_dict() for q in pagination.items],
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages
            },
            "stats": {
                "total_value": float(total_value),
                "this_month": this_month_count
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= GET SINGLE QUOTATION =================
@quotations_bp.route('/quotations/<int:id>', methods=['GET'])
def get_quotation(id):
    quotation = Quotation.query.get_or_404(id)
    return jsonify(quotation.to_dict()), 200


# ================= CREATE QUOTATION =================
# ================= CREATE QUOTATION =================
@quotations_bp.route('/quotations', methods=['POST'])
def create_quotation():
    try:
        data = request.get_json()
        errors = validate_quotation_data(data)
        if errors:
            return jsonify({"errors": errors}), 400

        customer = data.get("customerInfo", {})
        totals = data.get("totals", {})

        # Handle estimate date conversion
        estimate_date = None
        if customer.get("estimateDate"):
            try:
                estimate_date = datetime.strptime(customer.get("estimateDate"), '%Y-%m-%d').date()
            except ValueError:
                estimate_date = None

        quotation = Quotation(
            quotation_no=generate_quotation_number(),
            quotation_date=date.today(),
            bill_to=customer.get("billTo"),
            contact_no=customer.get("contactNo"),
            state_name=customer.get("stateName"),
            customer_gstin=customer.get("gstin"),
            estimate_no=customer.get("estimateNo"),
            estimate_date=estimate_date,  # Save estimate date
            company_name=DEFAULT_COMPANY_INFO["name"],
            company_address=DEFAULT_COMPANY_INFO["address"],
            company_phone=DEFAULT_COMPANY_INFO["phone"],
            company_gstin=DEFAULT_COMPANY_INFO["gstin"],
            company_branch=DEFAULT_COMPANY_INFO["branch"],
            total_amount=totals.get("totalAmount", 0),
            cgst=totals.get("cgst", 0),
            sgst=totals.get("sgst", 0),
            grand_total=totals.get("grandTotal", 0),
        )

        db.session.add(quotation)
        db.session.flush()

        for i, item in enumerate(data.get("items", [])):
            db.session.add(QuotationItem(
                quotation_id=quotation.id,
                description=item.get("description"),
                quantity=item.get("qty"),
                rate=item.get("rate"),
                amount=item.get("amount"),
                item_order=i
            ))

        db.session.commit()
        return jsonify({"message": "Quotation created"}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Duplicate quotation"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ================= UPDATE QUOTATION =================
@quotations_bp.route('/quotations/<int:id>', methods=['PUT'])
def update_quotation(id):
    try:
        quotation = Quotation.query.get_or_404(id)
        data = request.get_json()

        errors = validate_quotation_data(data)
        if errors:
            return jsonify({"errors": errors}), 400

        customer = data.get("customerInfo", {})
        totals = data.get("totals", {})

        # Handle estimate date conversion
        estimate_date = None
        if customer.get("estimateDate"):
            try:
                estimate_date = datetime.strptime(customer.get("estimateDate"), '%Y-%m-%d').date()
            except ValueError:
                estimate_date = None

        # Update quotation fields
        quotation.bill_to = customer.get("billTo")
        quotation.contact_no = customer.get("contactNo")
        quotation.state_name = customer.get("stateName")
        quotation.customer_gstin = customer.get("gstin")
        quotation.estimate_no = customer.get("estimateNo")
        quotation.estimate_date = estimate_date  # Update estimate date
        quotation.total_amount = totals.get("totalAmount", 0)
        quotation.cgst = totals.get("cgst", 0)
        quotation.sgst = totals.get("sgst", 0)
        quotation.grand_total = totals.get("grandTotal", 0)
        quotation.updated_at = datetime.utcnow()

        # Delete old items
        QuotationItem.query.filter_by(quotation_id=quotation.id).delete()

        # Add new items
        for i, item in enumerate(data.get("items", [])):
            db.session.add(QuotationItem(
                quotation_id=quotation.id,
                description=item.get("description"),
                quantity=item.get("qty"),
                rate=item.get("rate"),
                amount=item.get("amount"),
                item_order=i
            ))

        db.session.commit()
        return jsonify({"message": "Quotation updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ================= COMPANY INFO =================
@quotations_bp.route('/company/info', methods=['GET'])
def get_company_info():
    return jsonify(DEFAULT_COMPANY_INFO), 200


# ================= HEALTH =================
@quotations_bp.route('/health', methods=['GET'])
def health():
    try:
        db.session.execute("SELECT 1")
        return jsonify({"status": "OK"}), 200
    except Exception as e:
        return jsonify({"status": "DB ERROR", "error": str(e)}), 500
# ================= GET QUOTATION BY QUOTATION NUMBER =================
@quotations_bp.route('/quotations/number/<string:quotation_no>', methods=['GET'])
def get_quotation_by_number(quotation_no):
    try:
        quotation = Quotation.query.filter_by(
            quotation_no=quotation_no
        ).first()

        if not quotation:
            return jsonify({
                "error": "Quotation not found",
                "quotation_no": quotation_no
            }), 404

        return jsonify(quotation.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
