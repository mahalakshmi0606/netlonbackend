from datetime import datetime
from app import db   # ✅ IMPORTANT FIX


class Quotation(db.Model):
    __tablename__ = "quotations"

    id = db.Column(db.Integer, primary_key=True)
    quotation_no = db.Column(db.String(50), unique=True, nullable=False)
    quotation_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    # ================= CUSTOMER INFO =================
    bill_to = db.Column(db.String(200), nullable=False)
    state_name = db.Column(db.String(100))
    contact_no = db.Column(db.String(20))
    customer_gstin = db.Column(db.String(20))
    estimate_no = db.Column(db.String(50))
    estimate_date = db.Column(db.Date)

    # ================= COMPANY INFO =================
    company_name = db.Column(db.String(200))
    company_description = db.Column(db.Text)
    company_phone = db.Column(db.String(20))
    company_gstin = db.Column(db.String(20))
    company_address = db.Column(db.Text)
    company_branch = db.Column(db.String(100))

    # ================= TOTALS =================
    total_amount = db.Column(db.Float, default=0.0)
    cgst = db.Column(db.Float, default=0.0)
    sgst = db.Column(db.Float, default=0.0)
    grand_total = db.Column(db.Float, default=0.0)

    # ================= TIMESTAMPS =================
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # ================= RELATIONSHIP =================
    items = db.relationship(
        "QuotationItem",
        backref="quotation",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "quotation_no": self.quotation_no,
            "quotation_date": self.quotation_date.isoformat()
            if self.quotation_date
            else None,

            "customerInfo": {
                "billTo": self.bill_to,
                "stateName": self.state_name,
                "contactNo": self.contact_no,
                "gstin": self.customer_gstin,
                "estimateNo": self.estimate_no,
                "estimateDate": self.estimate_date.isoformat()
                if self.estimate_date
                else None,
            },

            "companyInfo": {
                "name": self.company_name,
                "description": self.company_description,
                "phone": self.company_phone,
                "gstin": self.company_gstin,
                "address": self.company_address,
                "branch": self.company_branch,
            },

            "items": [item.to_dict() for item in self.items],

            "totals": {
                "totalAmount": self.total_amount,
                "cgst": self.cgst,
                "sgst": self.sgst,
                "grandTotal": self.grand_total,
            },

            "created_at": self.created_at.isoformat()
            if self.created_at
            else None,
            "updated_at": self.updated_at.isoformat()
            if self.updated_at
            else None,
        }


class QuotationItem(db.Model):
    __tablename__ = "quotation_items"

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(
        db.Integer,
        db.ForeignKey("quotations.id", ondelete="CASCADE"),
        nullable=False,
    )

    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    rate = db.Column(db.Float, default=0.0)
    amount = db.Column(db.Float, default=0.0)
    item_order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "qty": self.quantity,
            "rate": self.rate,
            "amount": self.amount,
            "item_order": self.item_order,
        }
