from flask import render_template
from app.main import main_bp
from app.models.product import Product
from app.models.media import Banner, Project
from app.models.content import Blog
from sqlalchemy.orm import load_only


@main_bp.route('/')
def index():
    """Trang chủ"""
    # Lấy banners đang active
    banners = Banner.query.filter_by(is_active=True).order_by(Banner.order).all()

    # Lấy sản phẩm nổi bật (featured)
    featured_products = Product.query.filter_by(
        is_featured=True,
        is_active=True
    ).limit(3).all()

    # Lấy sản phẩm mới nhất
    latest_products = Product.query.filter_by(
        is_active=True
    ).order_by(Product.created_at.desc()).limit(3).all()

    # Lấy tin tức nổi bật
    featured_blogs = (Blog.query
                      .options(load_only(Blog.slug, Blog.title, Blog.created_at, Blog.image))
                      .filter_by(is_featured=True, is_active=True)
                      ).limit(3).all()

    featured_projects = Project.query.filter_by(is_featured=True, is_active=True).order_by(
        Project.created_at.desc()).limit(6).all()

    return render_template('public/index.html',
                           banners=banners,
                           featured_products=featured_products,
                           latest_products=latest_products,
                           featured_blogs=featured_blogs,
                           featured_projects=featured_projects)


@main_bp.route('/gioi-thieu')
def about():
    """Trang giới thiệu"""
    return render_template('public/about.html')


@main_bp.route('/chinh-sach')
def policy():
    """Trang chính sách"""
    return render_template('public/policy.html')
