from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponse
from django.db.models import Value
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Product, Collection, Review, Cart, CartItem, Customer, Order
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer, OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer
from .filters import ProductFilter
from .permissions import IsAdminOrReadOnly, IsAdminUser
import pprint
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_updated']

    def get_queryset(self):
        queryset = Product.objects.select_related('collection').all()
        # collection_id = self.request.query_params.get('collection_id')

        # if collection_id is not None:
        #     queryset = queryset.filter(collection_id=collection_id)

        # Only apply limit for list view
        # if self.action == 'list':
        #     return queryset[:21]

        return queryset

    def get_serializer_context(self):
        # not compulsory but recommended.
        # Especially if your serializer Generates full URLs or depends on request data
        return {'request': self.request}


class CollectionViewSet(ModelViewSet):
    # ReadOnlyModelViewSet for read only. No create, update or delete.
    queryset = Collection.objects.annotate(
        product_count=Count('product'))
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).exists() > 0:
            return Response({"error": "Cannot delete Collection because it contains some products"}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #     collection = get_object_or_404(Collection, pk=pk)
    #     if collection.product_set.count() > 0:
    #         return Response({"error": "Cannot delete Collection because it contains some products"}, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         collection.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['products_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['products_pk']}


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('cartitem_set__product').all()
    serializer_class = CartSerializer
    lookup_field = 'cart_id'


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    # queryset = CartItem.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        # return {'cart_id': self.kwargs['cart_cart_id']} #Ordinarily, but since cart_cart_id is a uuid, not id.
        # Get the UUID from URL

        if not hasattr(self, 'this_cart_id'):
            self.fetch_cart_id()

        return {'cart_id': self.this_cart_id}

    # Simply use UUID as Cart primary key to avoid all these complexity around get_queryset.
    """
    Using UUID as Cart primary key:
    def get_queryset(self):
        return CartItem.objects.filter(cart__cart_id=self.kwargs['cart_pk'])
    """
    # This current implementation is sending more queries to the db and I haven't figured how to solve it with select_/prefetch_related.

    def get_queryset(self):
        # Get the UUID from URL
        # cart_uuid = self.kwargs['cart_cart_id']

        self.fetch_cart_id()

        if self.this_cart_id is not None:
            return CartItem.objects.filter(cart_id=self.this_cart_id)
        else:
            return CartItem.objects.none()

        # Convert to internal Cart ID
        # try:
        #     cart = Cart.objects.get(cart_id=cart_uuid)
        #     self.this_cart_id = cart.id
        #     # Now filter by the internal ID (much simpler!)
        #     return CartItem.objects.filter(cart_id=cart.id)
        # except Cart.DoesNotExist:
        #     return CartItem.objects.none()

    def fetch_cart_id(self):
        # Get the UUID from URL
        cart_uuid = self.kwargs['cart_cart_id']

        # Convert to internal Cart ID
        try:
            cart = Cart.objects.get(cart_id=cart_uuid)
            self.this_cart_id = cart.id
        except Cart.DoesNotExist:
            # 404 error
            self.this_cart_id = None


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    # serializer_class = OrderSerializer

    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'customer_id': self.request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        customer_id = Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)

    # def get_serializer_context(self):
    #     return {'customer_id': self.request.user.id}

    # Not complete yet. Get queryset depending on is_staff or user


class UserAPIView(APIView):

    @swagger_auto_schema(
        responses={200: CustomerSerializer(many=True)}
    )
    def get(self, request):
        users = Customer.objects.all()  # Your queryset here
        serializer = CustomerSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CustomerSerializer,
        responses={201: CustomerSerializer}
    )
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            # Create user logic
            user_data = {'id': 1, **serializer.validated_data}
            return Response(CustomerSerializer(user_data).data, status=201)
        return Response(serializer.errors, status=400)


""" Deprecated """


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related(
        'collection').all()[:21]
    serializer_class = ProductSerializer


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductList_before_mixins(APIView):
    def get(self, request):
        queryset = Product.objects.select_related(
            'collection').all()[:21]
        products = get_list_or_404(queryset)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Ok")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail_before_mixins(APIView):

    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(
            product_count=Count('product'))
        collections = get_list_or_404(queryset)
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, id):
    queryset = Collection.objects.annotate(
        product_count=Count('product'))
    collection = get_object_or_404(queryset, pk=id)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.product_set.count() > 0:
            return Response({"error": "Cannot delete Collection because it contains some products"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            collection.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
