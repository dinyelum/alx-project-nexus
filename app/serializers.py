from decimal import Decimal
from django.db import transaction
from .models import Product, Collection, Review, Cart, CartItem, Customer, Order, OrderItem
from rest_framework import serializers
import sys
import pprint


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'product_count']

    product_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description',
                  'inventory', 'price', 'price_with_tax', 'collection']
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField('calculate_tax')
    collection = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all()
    )

    def calculate_tax(self, product: Product):
        return round(product.unit_price * Decimal(1.1), 2)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField('calculate_total_price')

    def calculate_total_price(self, cartitem: CartItem):
        return cartitem.product.unit_price * cartitem.quantity


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'cart_id', 'items', 'total_price']

    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    items = CartItemSerializer(
        many=True, source='cartitem_set', read_only=True)
    total_price = serializers.SerializerMethodField('calculate_total_price')

    def calculate_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.cartitem_set.all()])


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                'No product with given ID was found.')
        return value

    def save(self):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)
        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['phone', 'birth_date', 'membership', 'user_id']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']

    items = OrderItemSerializer(many=True, source='orderitem_set')


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']


class CreateOrderSerializer(serializers.Serializer):
    cart_uuid = serializers.UUIDField()

    def validate_cart_uuid(self, cart_uuid):
        db_cart_id = Cart.objects.filter(
            cart_id=cart_uuid).values_list('id', flat=True).first()
        if db_cart_id is None:
            raise serializers.ValidationError(
                'No cart with the given id was found.')
        if CartItem.objects.filter(cart_id=db_cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return db_cart_id

    def save(self, **kwargs):
        db_cart_id = self.validated_data['cart_uuid']
        with transaction.atomic():
            customer = Customer.objects.get(
                user_id=self.context['customer_id'])
            order = Order.objects.create(customer=customer)

            # db_cart_id = Cart.objects.filter(
            #     cart_id=self.validated_data['cart_uuid']).values_list('id', flat=True).first()

            cart_items = CartItem.objects.select_related('product').filter(
                cart_id=db_cart_id)

            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=db_cart_id).delete()

            return order
