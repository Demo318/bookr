# Generated by Django 4.0 on 2024-04-08 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('reviews', '0001_initial'), ('reviews', '0002_book_contributor_review_bookcontributor_and_more'), ('reviews', '0003_book_cover_book_sample_alter_book_isbn')]

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the Publisher.', max_length=50)),
                ('website', models.URLField(help_text="The Publisher's website.")),
                ('email', models.EmailField(help_text="The Publisher's email address.", max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='The title of the book.', max_length=70)),
                ('publication_date', models.DateField(verbose_name='Date the book was published.')),
                ('isbn', models.CharField(max_length=20, verbose_name='ISBN number of the book.')),
            ],
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_names', models.CharField(help_text="The contributor's first name or names.", max_length=50)),
                ('last_names', models.CharField(help_text="The contributor's last name or names.", max_length=50)),
                ('email', models.EmailField(help_text='The contact email for the contributor.', max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(help_text='The Review text.')),
                ('rating', models.IntegerField(help_text='The rating the reviewer has given.')),
                ('date_created', models.DateTimeField(auto_now_add=True, help_text='The date and time the review was created.')),
                ('date_edited', models.DateTimeField(help_text='The date and time the review was last edited.', null=True)),
                ('book', models.ForeignKey(help_text='The Book that this review is for.', on_delete=django.db.models.deletion.CASCADE, to='reviews.book')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='BookContributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('AUTHOR', 'Author'), ('CO_AUTHOR', 'Co-Author'), ('EDITOR', 'Editor')], max_length=20, verbose_name='The role this contributor had in the book')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.book')),
                ('contributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.contributor')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='contributors',
            field=models.ManyToManyField(through='reviews.BookContributor', to='reviews.Contributor'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.publisher'),
        ),
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='book_covers/'),
        ),
        migrations.AddField(
            model_name='book',
            name='sample',
            field=models.FileField(blank=True, null=True, upload_to='book_samples/'),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(blank=True, max_length=20, verbose_name='ISBN number of the book.'),
        ),
    ]
