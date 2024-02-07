{
  "openapi": "3.0.3",
  "info": {
    "title": "eCommerce Application - OpenAPI 3.0",
    "description": "This is an online shopping application Server API Documentation! Our server, built on the OpenAPI 3.0 specification drives an exceptional online shopping platform. Embracing a design-first approach, we continuously enhance our API to deliver seamless experiences. You can find out more about online store at [https://onlinestore](https://onlinestore.iio)\n \n \n",
    "termsOfService": "http://swagger.io/terms/",
    "contact": {
      "email": "me@alvinombito.com"
    },
    "license": {
      "name": "Apache 2.0",
      "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
    },
    "version": "1.0.11"
  },
  "externalDocs": {
    "description": "Find out more about Swagger",
    "url": "http://swagger.io"
  },
  "servers": [
    {
      "url": "http://localhost:5555"
    }
  ],
  "tags": [
    {
      "name": "home",
      "description": "Home route"
    },
    {
      "name": "products",
      "description": "Everything about our products",
      "externalDocs": {
        "description": "Find out more",
        "url": "http://swagger.i"
      }
    },
    {
      "name": "user",
      "description": "Operations about user"
    },
    {
      "name": "orders",
      "description": "Operations related to orders"
    },
    {
      "name": "reviews",
      "description": "Operations related to reviews"
    },
    {
      "name": "favourites",
      "description": "Operations related to favourites"
    }
  ],
  "paths": {
    "/": {
      "get": {
        "tags": [
          "home"
        ],
        "summary": "Landing page",
        "description": "This endpoint is the landing page to our server",
        "operationId": "findPetsByStatus",
        "parameters": [
          {
            "name": "status",
            "in": "query",
            "description": "Status values that need to be considered for filter",
            "required": false,
            "explode": true,
            "schema": {
              "type": "string",
              "default": "available",
              "enum": [
                "available",
                "pending",
                "sold"
              ]
            }
          }
        ],
        "responses": {
          "200": {
            "description": "successful operation",
            "content": {
              "application/json": {
                "schema": {
                  "type": "string"
                }
              }
            }
          },
          "400": {
            "description": "Invalid status value"
          }
        }
      }
    },
    "/products": {
      "get": {
        "tags": [
          "products"
        ],
        "summary": "Get a list of all products",
        "description": "This endpoint uses a get request to fetch all products",
        "operationId": "getAllProducts",
        "parameters": [
          {
            "name": "status",
            "in": "query",
            "description": "Status values that need to be considered for filter",
            "required": false,
            "explode": true,
            "schema": {
              "type": "string",
              "default": "available",
              "enum": [
                "available",
                "pending",
                "sold"
              ]
            }
          }
        ],
        "responses": {
          "200": {
            "description": "successful operation",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/Products"
                  }
                }
              },
              "application/xml": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/Products"
                  }
                }
              }
            }
          },
          "400": {
            "description": "Invalid status value"
          }
        }
      }
    },
    "/products/{product.id}": {
      "get": {
        "tags": [
          "products"
        ],
        "summary": "Finds Products by ID",
        "description": "Multiple tags can be provided with comma-separated strings. Use tag1, tag2, tag3 for testing.",
        "operationId": "getProductById",
        "parameters": [
          {
            "name": "product_id",
            "in": "path",
            "description": "ID of the product to fetch",
            "required": true,
            "schema": {
              "type": "integer",
              "format": "int64"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "successful operation",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Products"
                }
              },
              "application/xml": {
                "schema": {
                  "$ref": "#/components/schemas/Products"
                }
              }
            }
          },
          "400": {
            "description": "Invalid product ID"
          }
        },
        "security": [
          {
            "petstore_auth": [
              "write:pets",
              "read:pets"
            ]
          }
        ]
      },
      "post": {
        "tags": [
          "products"
        ],
        "summary": "Add a new product to the store",
        "description": "Add a new pet to the store",
        "operationId": "addProduct",
        "requestBody": {
          "description": "Create a new product in the store",
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/Products"
              }
            },
            "application/xml": {
              "schema": {
                "$ref": "#/components/schemas/Products"
              }
            },
            "application/x-www-form-urlencoded": {
              "schema": {
                "$ref": "#/components/schemas/Products"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "description": "Successful operation",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Products"
                }
              },
              "application/xml": {
                "schema": {
                  "$ref": "#/components/schemas/Products"
                }
              }
            }
          },
          "400": {
            "description": "Invalid input"
          },
          "422": {
            "description": "Validation exception"
          }
        },
        "security": [
          {
            "petstore_auth": [
              "write:pets",
              "read:pets"
            ]
          }
        ]
      },
      "delete": {
        "tags": [
          "products"
        ],
        "summary": "Delete a product by ID",
        "description": "For valid response try integer IDs with value < 1000. Anything above 1000 or non-integers will generate API errors",
        "operationId": "deleteProduct",
        "parameters": [
          {
            "name": "product_id",
            "in": "path",
            "description": "ID of the product that needs to be deleted",
            "required": true,
            "schema": {
              "type": "integer",
              "format": "int64"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful operation"
          },
          "404": {
            "description": "Product not found"
          }
        }
      }
    },
    "/users": {
      "get": {
        "tags": [
          "user"
        ],
        "summary": "Get a list of all users",
        "description": "This endpoint uses a get request to fetch all products",
        "operationId": "findUsers",
        "parameters": [
          {
            "name": "status",
            "in": "query",
            "description": "Status values that need to be considered for filter",
            "required": false,
            "explode": true,
            "schema": {
              "type": "string",
              "default": "available",
              "enum": [
                "available",
                "pending",
                "sold"
              ]
            }
          }
        ],
        "responses": {
          "200": {
            "description": "successful operation",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/User"
                  }
                }
              },
              "application/xml": {
                "schema": {
                  "$ref": "#/components/schemas/User"
                }
              }
            }
          },
          "400": {
            "description": "Invalid status value"
          }
        },
        "security": [
          {
            "petstore_auth": [
              "write:pets",
              "read:pets"
            ]
          }
        ]
      }
    },
    "/signup_user": {
      "post": {
        "tags": [
          "user"
        ],
        "summary": "Create a new user",
        "description": "A post request to sign up user.",
        "operationId": "createUser",
        "requestBody": {
          "description": "Created user object",
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/User"
              }
            },
            "application/xml": {
              "schema": {
                "$ref": "#/components/schemas/User"
              }
            },
            "application/x-www-form-urlencoded": {
              "schema": {
                "$ref": "#/components/schemas/User"
              }
            }
          }
        },
        "responses": {
          "default": {
            "description": "successful operation",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/User"
                }
              },
              "application/xml": {
                "schema": {
                  "$ref": "#/components/schemas/User"
                }
              }
            }
          }
        }
      }
    },
    "/login_user": {
      "post": {
        "tags": [
          "user"
        ],
        "summary": "Login user",
        "description": "Logs user into the system",
        "operationId": "loginUser",
        "requestBody": {
          "description": "Created user object",
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/User"
              }
            },
            "application/xml": {
              "schema": {
                "$ref": "#/components/schemas/User"
              }
            },
            "application/x-www-form-urlencoded": {
              "schema": {
                "$ref": "#/components/schemas/User"
              }
            }
          }
        },
        "responses": {
          "default": {
            "description": "successful operation",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/User"
                }
              },
              "application/xml": {
                "schema": {
                  "$ref": "#/components/schemas/User"
                }
              }
            }
          }
        }
      }
    },
    "/logout_user": {
      "post": {
        "tags": [
          "user"
        ],
        "summary": "Logs out current logged-in user session",
        "description": "Logs user into the system",
        "operationId": "logoutUser",
        "requestBody": {
          "description": "Created user object",
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/User"
              }
            },
            "application/xml": {
              "schema": {
                "$ref": "#/components/schemas/User"
              }
            },
            "application/x-www-form-urlencoded": {
              "schema": {
                "$ref": "#/components/schemas/User"
              }
            }
          }
        },
        "responses": {
          "default": {
            "description": "successful operation",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/User"
                }
              },
              "application/xml": {
                "schema": {
                  "$ref": "#/components/schemas/User"
                }
              }
            }
          }
        }
      }
    },
    "/user/{id}": {
      "get": {
        "tags": [
          "user"
        ],
        "summary": "Get user by user ID",
        "description": "",
        "operationId": "getUserById",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "The ID that needs to be fetched. Use user1 for testing.",
            "required": true,
            "schema": {
              "type": "integer",
              "format": "int64"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "successful operation",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/User"
                }
              },
              "application/xml": {
                "schema": {
                  "$ref": "#/components/schemas/User"
                }
              }
            }
          },
          "400": {
            "description": "Invalid ID supplied"
          },
          "404": {
            "description": "User not found"
          }
        }
      },
      "put": {
        "tags": [
          "user"
        ],
        "summary": "Update user",
        "description": "This can only be done by the logged-in user.",
        "operationId": "updateUser",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "ID of the user that needs to be updated",
            "required": true,
            "schema": {
              "type": "integer",
              "format": "int64"
            }
          }
        ],
        "requestBody": {
          "description": "Update an existing user in the store",
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/User"
              }
            },
            "application/xml": {
              "schema": {
                "$ref": "#/components/schemas/User"
              }
            },
            "application/x-www-form-urlencoded": {
              "schema": {
                "$ref": "#/components/schemas/User"
              }
            }
          }
        },
        "responses": {
          "default": {
            "description": "successful operation"
          }
        }
      },
      "delete": {
        "tags": [
          "user"
        ],
        "summary": "Delete user",
        "description": "This can only be done by the logged-in user.",
        "operationId": "deleteUser",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "The ID that needs to be deleted",
            "required": true,
            "schema": {
              "type": "integer",
              "format": "int64"
            }
          }
        ],
        "responses": {
          "400": {
            "description": "Invalid ID supplied"
          },
          "404": {
            "description": "User not found"
          }
        }
      }
    },
    "/orders": {
      "get": {
        "tags": [
          "orders"
        ],
        "summary": "Fetch all orders",
        "description": "Returns a single order",
        "operationId": "getOrderById",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "ID of order to return",
            "required": true,
            "schema": {
              "type": "integer",
              "format": "int64"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "successful operation",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Order"
                }
              },
              "application/xml": {
                "schema": {
                  "$ref": "#/components/schemas/Order"
                }
              }
            }
          },
          "400": {
            "description": "Invalid ID supplied"
          },
          "404": {
            "description": "Order not found"
          }
        },
        "security": [
          {
            "api_key": []
          },
          {
            "petstore_auth": [
              "write:pets",
              "read:pets"
            ]
          }
        ]
      }
    },
    "/orders/{id}": {
      "get": {
        "tags": [
          "orders"
        ],
        "summary": "Find order by ID",
        "description": "Returns a single order",
        "operationId": "getOrderById",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "ID of order to return",
            "required": true,
            "schema": {
              "type": "integer",
              "format": "int64"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "successful operation",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Order"
                }
              },
              "application/xml": {
                "schema": {
                  "$ref": "#/components/schemas/Order"
                }
              }
            }
          },
          "400": {
            "description": "Invalid ID supplied"
          },
          "404": {
            "description": "Order not found"
          }
        },
        "security": [
          {
            "api_key": []
          },
          {
            "petstore_auth": [
              "write:pets",
              "read:pets"
            ]
          }
        ]
      },
      "delete": {
        "tags": [
          "orders"
        ],
        "summary": "Deletes an order",
        "description": "Delete an order",
        "operationId": "deleteOrder",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "Order ID to delete",
            "required": true,
            "schema": {
              "type": "integer",
              "format": "int64"
            }
          }
        ],
        "responses": {
          "400": {
            "description": "Invalid order ID"
          }
        },
        "security": [
          {
            "petstore_auth": [
              "write:pets",
              "read:pets"
            ]
          }
        ]
      },
      "post": {
        "tags": [
          "orders"
        ],
        "summary": "Create an order",
        "description": "",
        "operationId": "createOrder",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "ID of pet to order",
            "required": true,
            "schema": {
              "type": "integer",
              "format": "int64"
            }
          },
          {
            "name": "additionalMetadata",
            "in": "query",
            "description": "Additional Metadata",
            "required": false,
            "schema": {
              "type": "string"
            }
          }
        ],
        "requestBody": {
          "content": {
            "application/octet-stream": {
              "schema": {
                "type": "string",
                "format": "binary"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "successful operation",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Order"
                }
              }
            }
          }
        },
        "security": [
          {
            "petstore_auth": [
              "write:pets",
              "read:pets"
            ]
          }
        ]
      }
    },
    "/reviews/{id}": {
      "get": {
        "tags": [
          "reviews"
        ],
        "summary": "Find review by product",
        "description": "Returns reviews of a single product",
        "operationId": "getOrderById",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "ID of order to return",
            "required": true,
            "schema": {
              "type": "integer",
              "format": "int64"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "successful operation",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Review"
                }
              },
              "application/xml": {
                "schema": {
                  "$ref": "#/components/schemas/Review"
                }
              }
            }
          },
          "400": {
            "description": "Invalid ID supplied"
          },
          "404": {
            "description": "Order not found"
          }
        },
        "security": [
          {
            "api_key": []
          },
          {
            "petstore_auth": [
              "write:pets",
              "read:pets"
            ]
          }
        ]
      },
      "post": {
        "tags": [
          "reviews"
        ],
        "summary": "Create a new review",
        "description": "",
        "operationId": "createOrder",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "ID of pet to order",
            "required": true,
            "schema": {
              "type": "integer",
              "format": "int64"
            }
          },
          {
            "name": "additionalMetadata",
            "in": "query",
            "description": "Additional Metadata",
            "required": false,
            "schema": {
              "type": "string"
            }
          }
        ],
        "requestBody": {
          "content": {
            "application/octet-stream": {
              "schema": {
                "type": "string",
                "format": "binary"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "successful operation",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Review"
                }
              }
            }
          }
        },
        "security": [
          {
            "petstore_auth": [
              "write:pets",
              "read:pets"
            ]
          }
        ]
      },
      "delete": {
        "tags": [
          "reviews"
        ],
        "summary": "Deletes a review",
        "description": "Delete a review",
        "operationId": "deleteOrder",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "Order ID to delete",
            "required": true,
            "schema": {
              "type": "integer",
              "format": "int64"
            }
          }
        ],
        "responses": {
          "400": {
            "description": "Invalid order ID"
          }
        },
        "security": [
          {
            "petstore_auth": [
              "write:pets",
              "read:pets"
            ]
          }
        ]
      }
    },
    "/favourite/{id}": {
      "get": {
        "tags": [
          "favourites"
        ],
        "summary": "Fetch all favourites by a user",
        "description": "Returns all favourites by a user",
        "operationId": "getOrderById",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "ID of order to return",
            "required": true,
            "schema": {
              "type": "integer",
              "format": "int64"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "successful operation",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Favourite"
                }
              },
              "application/xml": {
                "schema": {
                  "$ref": "#/components/schemas/Favourite"
                }
              }
            }
          },
          "400": {
            "description": "Invalid ID supplied"
          },
          "404": {
            "description": "Order not found"
          }
        },
        "security": [
          {
            "api_key": []
          },
          {
            "petstore_auth": [
              "write:pets",
              "read:pets"
            ]
          }
        ]
      },
      "post": {
        "tags": [
          "favourites"
        ],
        "summary": "Add a new favourite products",
        "description": "",
        "operationId": "createOrder",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "ID of pet to order",
            "required": true,
            "schema": {
              "type": "integer",
              "format": "int64"
            }
          },
          {
            "name": "additionalMetadata",
            "in": "query",
            "description": "Additional Metadata",
            "required": false,
            "schema": {
              "type": "string"
            }
          }
        ],
        "requestBody": {
          "content": {
            "application/octet-stream": {
              "schema": {
                "type": "string",
                "format": "binary"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "successful operation",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Favourite"
                }
              }
            }
          }
        },
        "security": [
          {
            "petstore_auth": [
              "write:pets",
              "read:pets"
            ]
          }
        ]
      },
      "delete": {
        "tags": [
          "favourites"
        ],
        "summary": "Removes a product from favourite",
        "description": "Delete a review",
        "operationId": "deleteOrder",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "Order ID to delete",
            "required": true,
            "schema": {
              "type": "integer",
              "format": "int64"
            }
          }
        ],
        "responses": {
          "400": {
            "description": "Invalid order ID"
          }
        },
        "security": [
          {
            "petstore_auth": [
              "write:pets",
              "read:pets"
            ]
          }
        ]
      }
    }
  },
  "components": {
    "schemas": {
      "Order": {
        "type": "object",
        "properties": {
          "id": {
            "type": "integer",
            "example": 5
          },
          "address": {
            "type": "string",
            "example": "Kilimani, Nairobi, Kenya"
          },
          "user_id": {
            "type": "integer",
            "example": 7
          },
          "total_amount": {
            "type": "integer",
            "example": 200
          },
          "order_date": {
            "type": "integer",
            "example": "9-7-2024"
          },
          "status": {
            "type": "string",
            "description": "Order Status",
            "example": "approved",
            "enum": [
              "placed",
              "approved",
              "delivered"
            ]
          },
          "shipping_fees": {
            "type": "integer",
            "example": 19
          }
        },
        "xml": {
          "name": "order"
        }
      },
      "Review": {
        "type": "object",
        "properties": {
          "id": {
            "type": "integer",
            "format": "int64",
            "example": 100000
          },
          "content": {
            "type": "string",
            "example": "I received my package while very fresh"
          },
          "rating": {
            "type": "integer",
            "example": 4
          },
          "product": {
            "type": "integer",
            "example": 1
          },
          "user": {
            "type": "integer",
            "example": 2
          }
        },
        "xml": {
          "name": "review"
        }
      },
      "OrderItem": {
        "type": "object",
        "properties": {
          "id": {
            "type": "integer",
            "format": "int64",
            "example": 1
          },
          "order_id": {
            "type": "integer",
            "example": 9
          },
          "product_id": {
            "type": "integer",
            "example": 1
          },
          "quantity": {
            "type": "integer",
            "example": 2
          },
          "subTotal_amount": {
            "type": "integer",
            "example": 200
          }
        },
        "xml": {
          "name": "orderitem"
        }
      },
      "Favourite": {
        "type": "object",
        "properties": {
          "id": {
            "type": "integer",
            "format": "int64",
            "example": 1
          },
          "product_id": {
            "type": "integer",
            "example": 3
          },
          "user_id": {
            "type": "integer",
            "example": 2
          }
        },
        "xml": {
          "name": "favourite"
        }
      },
      "User": {
        "type": "object",
        "properties": {
          "id": {
            "type": "integer",
            "format": "int64",
            "example": 10
          },
          "full_name": {
            "type": "string",
            "example": "Alvin"
          },
          "email": {
            "type": "string",
            "example": "alvin@gmail.com"
          },
          "phone_number": {
            "type": "string",
            "example": "254722222222"
          },
          "_password_hash": {
            "type": "string",
            "example": "$2b$12$EKRddzZQbP7mSbNHrD.pyuTGJr7NZHAfZsMOnmfd2tYKs5JMUj6mC"
          },
          "address": {
            "type": "string",
            "example": "Karen, Nairobi, Kenya"
          },
          "created_at": {
            "type": "integer",
            "example": "2-2-2024"
          }
        },
        "xml": {
          "name": "user"
        }
      },
      "Products": {
        "required": [
          "name",
          "photoUrls"
        ],
        "properties": {
          "id": {
            "type": "integer",
            "format": "int64",
            "example": 1
          },
          "name": {
            "type": "string",
            "example": "Ovacado"
          },
          "category": {
            "type": "string",
            "example": "Fruits"
          },
          "price": {
            "type": "integer",
            "example": 25
          },
          "description": {
            "type": "string",
            "example": "Well groomed ovacados"
          },
          "imageURL": {
            "type": "string",
            "example": "https://example.com/product1.jpg"
          },
          "reviews": {
            "type": "string",
            "example": "Well groomed ovacados"
          },
          "rating": {
            "type": "integer",
            "example": 4
          },
          "grouping": {
            "type": "string",
            "example": "Freshly stocked"
          }
        },
        "xml": {
          "name": "products"
        }
      }
    },
    "requestBodies": {
      "Pet": {
        "description": "Pet object that needs to be added to the store",
        "content": {
          "application/json": {
            "schema": {
              "$ref": "#/components/schemas/Products"
            }
          },
          "application/xml": {
            "schema": {
              "$ref": "#/components/schemas/Products"
            }
          }
        }
      },
      "UserArray": {
        "description": "List of user object",
        "content": {
          "application/json": {
            "schema": {
              "type": "array",
              "items": {
                "$ref": "#/components/schemas/User"
              }
            }
          }
        }
      }
    },
    "securitySchemes": {
      "petstore_auth": {
        "type": "oauth2",
        "flows": {
          "implicit": {
            "authorizationUrl": "https://petstore3.swagger.io/oauth/authorize",
            "scopes": {
              "write:pets": "modify pets in your account",
              "read:pets": "read your pets"
            }
          }
        }
      },
      "api_key": {
        "type": "apiKey",
        "name": "api_key",
        "in": "header"
      }
    }
  }
}