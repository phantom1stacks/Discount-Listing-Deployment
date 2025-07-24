from datetime import date, timedelta
from flask import (
    Flask, render_template, redirect, url_for, flash, request
)
from flask_login import (
    LoginManager, login_user, login_required, logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, Shop, Discount
from forms import RegisterForm, LoginForm, DiscountForm

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(shop_id):
        return Shop.query.get(int(shop_id))

    # FIXED: Replace @app.before_first_request with app_context
    with app.app_context():
        db.create_all()

    # ---------- Routes ----------
    @app.route("/")
    def index():
        q_date     = request.args.get("date", "all")
        q_category = request.args.get("cat", "all")
        query = Discount.query

        # Date filtering
        today = date.today()
        if q_date == "today":
            query = query.filter(Discount.start_date <= today,
                                 Discount.end_date >= today)
        elif q_date == "tomorrow":
            tomorrow = today + timedelta(days=1)
            query = query.filter(Discount.start_date <= tomorrow,
                                 Discount.end_date >= tomorrow)
        elif q_date == "week":
            week_end = today + timedelta(days=7)
            query = query.filter(Discount.start_date <= week_end,
                                 Discount.end_date >= today)

        # Category filtering
        if q_category != "all":
            query = query.filter_by(category=q_category)

        search_term = request.args.get("search")
        if search_term:
            like = f"%{search_term}%"
            query = query.join(Shop).filter(
                (Discount.product.ilike(like)) | (Shop.name.ilike(like))
            )

        discounts = query.order_by(Discount.percent_off.desc()).all()
        return render_template("index.html", discounts=discounts)

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        form = RegisterForm()
        if form.validate_on_submit():
            hashed = generate_password_hash(form.pwd.data)
            shop = Shop(name=form.name.data, email=form.email.data, password=hashed)
            db.session.add(shop)
            db.session.commit()
            flash("Registration successful. You can now log in.", "success")
            return redirect(url_for("login"))
        return render_template("register.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        form = LoginForm()
        if form.validate_on_submit():
            shop = Shop.query.filter_by(email=form.email.data).first()
            if shop and check_password_hash(shop.password, form.pwd.data):
                login_user(shop)
                return redirect(url_for("index"))
            flash("Invalid credentials.", "danger")
        return render_template("login.html", form=form)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("index"))

    @app.route("/discount/new", methods=["GET", "POST"])
    @login_required
    def add_discount():
        form = DiscountForm()
        if form.validate_on_submit():
            disc = Discount(
                product=form.product.data,
                percent_off=form.percent.data,
                category=form.category.data,
                start_date=form.start.data,
                end_date=form.end.data,
                city=form.city.data,
                shop_id=current_user.id
            )
            db.session.add(disc)
            db.session.commit()
            flash("Discount published!", "success")
            return redirect(url_for("index"))
        return render_template("add_discount.html", form=form)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
