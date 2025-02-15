# Generated by Django 5.0 on 2023-12-27 10:13

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dishes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'In progress'), (1, 'Completed')], default=0)),
                ('is_takeaway', models.IntegerField(choices=[(0, 'Here'), (1, 'Takeaway order')], default=0)),
                ('payment', models.IntegerField(choices=[(0, 'Cash'), (1, 'Terminal')], default=0)),
                ('total_price', models.PositiveIntegerField(blank=True, default=0, editable=False, null=True)),
            ],
            options={
                'db_table': 'order',
                'ordering': ['status', 'time_created'],
            },
        ),
        migrations.CreateModel(
            name='OrderComment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('body', models.TextField(default='-')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='orders.order')),
            ],
            options={
                'db_table': 'order_comment',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('additives', models.ManyToManyField(blank=True, to='dishes.additive')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dishes.dish')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
            ],
            options={
                'db_table': 'order_item',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'table',
                'ordering': ['id'],
                'indexes': [models.Index(fields=['id'], name='table_id_1be14a_idx')],
            },
        ),
        migrations.AddField(
            model_name='order',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='orders.table'),
        ),
    ]
