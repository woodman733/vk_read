# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SomeForm
import requests
import json
from config import Config
import re


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SomeForm()

    domain = "https://api.vk.com/method"
    access_token = Config.SECRET_KEY
    user_id = Config.USER_ID

    if form.validate_on_submit():
        flash('Get message for message_id: {}'.format(
            form.msg_id.data))

        query_params = {
            'domain': domain,
            'access_token': access_token,
            'user_id': Config.USER_ID,
            'message_ids': form.msg_id.data
        }

        query = "{domain}/messages.getById?message_ids={message_ids}&user_id={user_id}&access_token={" \
                "access_token}&v=5.53".format(**query_params)
        msg_body = requests.get(query).json()

        # data = json.dumps(msg_body)
        # obj0 = json.loads(data)
        # obj1 = (obj0["response"])
        # obj2 = (obj1["items"])
        # obj3 = (obj2[0])

        try:
            msg_text = ((((json.loads(json.dumps(msg_body))["response"])["items"])[0])["body"])
        except KeyError:
            msg_text = 'чет ошибка какая-то'

        try:
            msg_attachments = ((((((json.loads(json.dumps(msg_body))["response"])["items"])[0])["attachments"])[0])[
                'photo'])
        except KeyError:
            try:
                msg_attachments = ((((((json.loads(json.dumps(msg_body))["response"])["items"])[0])["attachments"])[0])[
                    'video'])
            except KeyError:
                msg_attachments = 'Медиа-вложений нет'

        # img_links = re.search(r'photo_', msg_attachments)

        return render_template('main.html', title='Main', form=form, msg_body=msg_body, user_id=user_id,
                               msg_text=msg_text, msg_attachments=msg_attachments)

    if form.validate_on_submit():
        flash('Get message for message_id: {}'.format(
            form.msg_id.data))
        # flash('length is: {}'.format(
        # form.length.data))
        return redirect(url_for('index'))
    return render_template('main.html', title='Main', form=form, user_id=user_id)
