from django.db import models



class Label(models.Model):
    label_id = models.AutoField('Lable id', primary_key=True)
    label_name = models.CharField('Lable Text', max_length=10)

    def __str__(self):
        return self.label_name

    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = 'Label'
        verbose_name_plural = 'Label'


class Book(models.Model):
    book_id = models.AutoField('BookID', primary_key=True)
    book_name = models.TextField('Book Name', max_length=50)
    book_author = models.TextField('Book author', max_length=50)
    book_avg_rating = models.IntegerField('Book rating')
    book_isbn = models.CharField('Book ISBN', max_length=30)
    book_language = models.CharField('Book Language', max_length=10)
    book_pages = models.IntegerField('Book Pages')
    book_numrating = models.IntegerField('Number of Rating')
    book_numtext = models.IntegerField('Number of Text')
    book_pubdate = models.DateField('Book publish data')
    book_publisher = models.CharField('Book publisher', max_length=30)
    book_img = models.CharField('Book Image', max_length=20)
    book_type = models.TextField('Book type', max_length=20)
    book_price = models.IntegerField('Book Price')
    book_bookstock = models.IntegerField('Book Stock', null=True, default=0)
    book_saleamount = models.IntegerField('Book sale amount')
    label = models.ForeignKey(Label, on_delete=models.CASCADE, verbose_name='book type id')

    def __str__(self):
        return self.book_name

    class Meta:
        verbose_name = 'Book Info'
        verbose_name_plural = 'Book Info'


class Dynamic(models.Model):
    dynamic_id = models.AutoField('Stat ID', primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='book title')
    dynamic_views = models.IntegerField('number of views')
    dynamic_search = models.IntegerField('number of searchs')
    dynamic_down = models.IntegerField('order time')

    class Meta:
        verbose_name = 'Stat'
        verbose_name_plural = 'Stat'


class Comment(models.Model):
    comment_id = models.AutoField('CommentID', primary_key=True)
    comment_text = models.CharField('Comment Text', max_length=500)
    comment_user = models.CharField('Comment User', max_length=20)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Book title')
    comment_date = models.CharField('date', max_length=50)
    comment_rate = models.FloatField('Rating', null=True, default=0)
    comment_tmp = models.IntegerField('Ratingtmp', null=True, default=0)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comment'


class Order(models.Model):
    order_id = models.AutoField('ID', primary_key=True)
    order_userid = models.TextField('UserID', max_length=20)
    order_date = models.DateField('Order Date')
    order_price = models.IntegerField('Order Price')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Order'


class Cart(models.Model):
    cart_id = models.AutoField('Cart ID', primary_key=True)
    cart_username = models.CharField("Cart User Name", max_length=50)
    cart_booktitle = models.CharField('Cart Book Title', max_length=150)
    cart_quantity = models.IntegerField('Cart Book quantity')
    cart_bookid = models.IntegerField('Cart Book Id')
    cart_bookprice = models.IntegerField('Cart Book Price')
    cart_publisher = models.CharField('Cart publisher', max_length=150)
    cart_bookrate = models.FloatField('Cart Book rate')
    cart_auther = models.CharField('Cart Book Price', max_length=150)
    status = models.IntegerField('Cart Book status')

    def total(self):
        return self.cart_quantity * self.cart_bookprice

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart'


class Recommend(models.Model):
    rec_id = models.AutoField('Id', primary_key=True)
    rec_auther = models.CharField('User', max_length=20)
    rec_type = models.CharField('Type', max_length=20)

    class Meta:
        verbose_name = 'Recommend'
        verbose_name_plural = 'Recommend'


class Orderinfo(models.Model):
    order_id = models.IntegerField('order id')
    order_name = models.CharField('order username', max_length=50)
    order_auther = models.CharField('auther', max_length=50)
    order_time = models.DateField('time')
    order_publisher = models.CharField('publisher', max_length=50)
    order_booktitle = models.CharField('titel', max_length=50)
    order_bookqua = models.IntegerField('quantity')
    order_bookprice = models.IntegerField('bookprice')
    order_bookrate = models.FloatField('bookrate')

    class Meta:
        # information of order
        verbose_name = 'info order'
        verbose_name_plural = 'info order'


class Userrela(models.Model):
    userrela_userid1 = models.TextField('User ID 1', max_length=30)
    userrela_userid2 = models.TextField('User ID 2', max_length=30)
    userrela_relation = models.IntegerField('Relation')

    def __str__(self):
        return self.userrela_userid1, self.userrela_userid2, self.userrela_relation

    class Meta:
        # information of order
        verbose_name = 'User Relation'
        verbose_name_plural = 'User Relation'


class Author(models.Model):
    author_author1 = models.TextField('Author name 1', max_length=30)
    author_author2 = models.TextField("Author name 2", max_length=30)
    author_degree = models.IntegerField("author degree")
    author_id = models.AutoField("degree id", primary_key=True)

    def __str__(self):
        return self.author_degree, self.author_author1, self.author_author1

    class Meta:
        verbose_name = "Author Degree"
        verbose_name_plural = "Author Degree"
