<a name="top"></a>
# Pricing Service v0.1.0

Microservicio de Precios

- [Discount](#discount)
	- [Create Discount](#create-discount)
	- [Delete a Discount](#delete-a-discount)
	- [Discount Price](#discount-price)
	- [Update Price](#update-price)
	
- [Price](#price)
	- [Create Price](#create-price)
	- [Delete a Price](#delete-a-price)
	- [Get Price](#get-price)
	- [Get Price History](#get-price-history)
	- [Update Price](#update-price)
	
- [RabbitMQ_GET](#rabbitmq_get)
	- [Logout](#logout)
	


# <a name='discount'></a> Discount

## <a name='create-discount'></a> Create Discount
[Back to top](#top)



	POST /v1/pricing/



### Examples

Body

```
{
    “discount_name”: “{Nombre del descuento}”,
    “discount_value”: “{Porcentaje de descuento}”,
    “discount_code”: “{Codigo de descuento}”,
    “visibility”: “{Si es publico, privado, etc}”,
    “validFrom”: “{Fecha de inicio de validez}”,
    “validTo”: “{Fecha de fin de validez}”,
    "article_id": “{ID del articulo}”,
    "state": “{Estado del descuento}”
}
```
Header Autorización

```
Authorization=bearer {token}
```


### Success Response

Respuesta

```
HTTP/1.1 200 OK
{
    “discount_id”: “{ID del descuento}”,
    “discount_name”: “{Nombre del descuento}”,
    “discount_value”: “{Porcentaje de descuento}”,
    “discount_code”: “{Codigo de descuento}”,
    “visibility”: “{Si es publico, privado, etc}”,
    “validFrom”: “{Fecha de inicio de validez}”,
    “validTo”: “{Fecha de fin de validez}”,
    "created": “{Fecha Hora de Creacion}”,
    “updated”: “{Fecha Hora de Actualizacion}”,
    "article_id": "{ID del producto}"
}
```


### Error Response

401 Unauthorized

```
HTTP/1.1 401 Unauthorized
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "path" : "{Nombre de la propiedad}",
    "message" : "{Motivo del error}"
}
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```
500 Server Error

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```
## <a name='delete-a-discount'></a> Delete a Discount
[Back to top](#top)



	DELETE /pricing/:discount_id/discount



### Examples

Header Autorización

```
Authorization=bearer {token}
```


### Success Response

200 Respuesta

```
HTTP/1.1 200 OK
```


### Error Response

401 Unauthorized

```
HTTP/1.1 401 Unauthorized
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "path" : "{Nombre de la propiedad}",
    "message" : "{Motivo del error}"
}
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```
500 Server Error

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```
## <a name='discount-price'></a> Discount Price
[Back to top](#top)



	GET /v1/pricing/:article_id





### Success Response

Response

```
HTTP/1.1 200 OK
{
"pagination": {
    "object_count": “{Numero de objetos en todas las paginas}”,
    "page_count": “{Numero de total de paginas}”,
    "page_size": “{Numero maximo de objetos en una response}”,
    "has_more_items": “{Si se puede seguir pidiendo valores a la API}”,
    "page_number": “{Numero de pagina actual}”,
    "article_id": "{ID del producto}"
    "discounts": [
    {
        “id_discount”: “{ID del descuento}”,
        “discount_name”: “{Nombre del descuento}”,
        “discount_value”: “{Porcentaje de descuento}”,
        “discount_code”: “{Codigo de descuento}”,
        “visibility”: “{Si es publico, privado, etc}”,
        “validFrom”: “{Fecha de inicio de validez}”,
        “validTo”: “{Fecha de fin de validez}”,
    }, ….
    ]
}
```


### Error Response

400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "path" : "{Nombre de la propiedad}",
    "message" : "{Motivo del error}"
}
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```
500 Server Error

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```
## <a name='update-price'></a> Update Price
[Back to top](#top)



	POST /v1/pricing/:discount_id/discount



### Examples

Body

```
{
    “discount_name”: “{Nombre del descuento}”,
    “discount_value”: “{Porcentaje de descuento}”,
    “discount_code”: “{Codigo de descuento}”,
    “visibility”: “{Si es publico, privado, etc}”,
    “validFrom”: “{Fecha de inicio de validez}”,
    “validTo”: “{Fecha de fin de validez}”,
    "article_id": “{ID del articulo}”,
    "state": “{Estado del descuento}”
}
```
Header Autorización

```
Authorization=bearer {token}
```


### Success Response

Respuesta

```
HTTP/1.1 200 OK
{
    “discount_id”: “{ID del descuento}”,
    “discount_name”: “{Nombre del descuento}”,
    “discount_value”: “{Porcentaje de descuento}”,
    “discount_code”: “{Codigo de descuento}”,
    “visibility”: “{Si es publico, privado, etc}”,
    “validFrom”: “{Fecha de inicio de validez}”,
    “validTo”: “{Fecha de fin de validez}”,
    "article_id": “{ID del articulo}”,
    "state": “{Estado del descuento}”
    "created": {Created Date}
}
```


### Error Response

401 Unauthorized

```
HTTP/1.1 401 Unauthorized
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "path" : "{Nombre de la propiedad}",
    "message" : "{Motivo del error}"
}
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```
500 Server Error

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```
# <a name='price'></a> Price

## <a name='create-price'></a> Create Price
[Back to top](#top)



	POST /v1/pricing/



### Examples

Body

```
{
    "max_price": {Max Price}
    "min_price": {Min Price}
    "price": {Current price},
    "price_currency": {Price Currency}
    "article_id": "{Article Id}"
}
```
Header Autorización

```
Authorization=bearer {token}
```


### Success Response

Respuesta

```
HTTP/1.1 200 OK
{
    "price_id": "{Price Id}"
    "max_price": {Max Price}
    "min_price": {Min Price}
    "price": {Current price},
    "price_currency": {Price Currency}
    "formated_price": {Formated Price}
    "article_id": "{Article Id}"
    "created": {Created Date}
    "updated": {Updated Date}
}
```


### Error Response

401 Unauthorized

```
HTTP/1.1 401 Unauthorized
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "path" : "{Nombre de la propiedad}",
    "message" : "{Motivo del error}"
}
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```
500 Server Error

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```
## <a name='delete-a-price'></a> Delete a Price
[Back to top](#top)



	DELETE /pricing/:article_id



### Examples

Header Autorización

```
Authorization=bearer {token}
```


### Success Response

200 Respuesta

```
HTTP/1.1 200 OK
```


### Error Response

401 Unauthorized

```
HTTP/1.1 401 Unauthorized
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "path" : "{Nombre de la propiedad}",
    "message" : "{Motivo del error}"
}
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```
500 Server Error

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```
## <a name='get-price'></a> Get Price
[Back to top](#top)



	GET /v1/pricing/:article_id





### Success Response

Response

```
HTTP/1.1 200 OK
{
    “discount_id”: “{ID del descuento}”,
    “discount_name”: “{Nombre del descuento}”,
    “discount_value”: “{Porcentaje de descuento}”,
    “discount_code”: “{Codigo de descuento}”,
    “visibility”: “{Si es publico, privado, etc}”,
    “validFrom”: “{Fecha de inicio de validez}”,
    “validTo”: “{Fecha de fin de validez}”,
    created: “{Fecha de creacion}”,
}
```


### Error Response

400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "path" : "{Nombre de la propiedad}",
    "message" : "{Motivo del error}"
}
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```
500 Server Error

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```
## <a name='get-price-history'></a> Get Price History
[Back to top](#top)



	GET /v1/pricing/:article_id





### Success Response

Response

```
HTTP/1.1 200 OK
{
"pagination": {
    "object_count": “{Numero de objetos en todas las paginas}”,
    "page_count": “{Numero de total de paginas}”,
    "page_size": “{Numero maximo de objetos en una response}”,
    "has_more_items": “{Si se puede seguir pidiendo valores a la API}”,
    "page_number": “{Numero de pagina actual}”,
    "article_id": "{ID del producto}"
    "price_schema": [
    {
        "_id": "{Price Id}"
        "created": {Creation Date}
        "state": {Price State}
        "max_price": {Max Price}
        "min_price": {Min Price}
        "price": {Current price},
        "price_currency": {Price Currency}
        "formated_price": {Formated Price}
    }, ….
    ]
}
```


### Error Response

400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "path" : "{Nombre de la propiedad}",
    "message" : "{Motivo del error}"
}
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```
500 Server Error

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```
## <a name='update-price'></a> Update Price
[Back to top](#top)



	POST /v1/pricing/:article_id



### Examples

Body

```
{
    "max_price": {Max Price}
    "min_price": {Min Price}
    "price": {Current price},
    "price_currency": {Price Currency}
    "price_id": "{Price Id}"
}
```
Header Autorización

```
Authorization=bearer {token}
```


### Success Response

Respuesta

```
HTTP/1.1 200 OK
{
    "price_id": "{Price Id}"
    "max_price": {Max Price}
    "min_price": {Min Price}
    "price": {Current price},
    "price_currency": {Price Currency}
    "formated_price": {Formated Price}
    "article_id": "{Article Id}"
    "created": {Created Date}
    "updated": {Updated Date}
}
```


### Error Response

401 Unauthorized

```
HTTP/1.1 401 Unauthorized
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "path" : "{Nombre de la propiedad}",
    "message" : "{Motivo del error}"
}
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```
500 Server Error

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```
# <a name='rabbitmq_get'></a> RabbitMQ_GET

## <a name='logout'></a> Logout
[Back to top](#top)

<p>Escucha de mensajes logout desde auth. Invalida sesiones en cache.</p>

	FANOUT auth/logout



### Examples

Mensaje

```
{
  "type": "article-exist",
  "message" : "tokenId"
}
```




