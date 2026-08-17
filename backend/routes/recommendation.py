from flask import Blueprint, render_template

bp = Blueprint("recommended", __name__)

@bp.route('/recommendation', methods=['GET'])
def result():
    return render_template('recommendation.html')