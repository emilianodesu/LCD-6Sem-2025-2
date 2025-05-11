// init-gymdata.js
// ----------------------------------------------------
// Al ejecutarse, 'db' apunta a la BD gymdata
// ----------------------------------------------------
db = db.getSiblingDB("gymdata");

// 1) Colección "users"
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "nombre",
        "email",
        "role",
        "direccion",
        "createdAt",
        "updatedAt",
      ],
      properties: {
        nombre: { bsonType: "string" },
        email: { bsonType: "string" },
        favoritos: { bsonType: "array", items: { bsonType: "objectId" } },
        role: { enum: ["user", "owner"] },
        createdAt: { bsonType: "date" },
        updatedAt: { bsonType: "date" },
        direccion: {
          bsonType: "object",
          // 'ubicacion' is now required within 'direccion' for the index
          required: ["ubicacion"],
          properties: {
            calle: { bsonType: "string" },
            estado: { bsonType: "string" },
            municipio: { bsonType: "string" },
            // Define 'ubicacion' as a GeoJSON Point
            ubicacion: {
              bsonType: "object",
              required: ["type", "coordinates"],
              properties: {
                type: {
                  enum: ["Point"],
                  description: "Must be 'Point' for GeoJSON",
                },
                coordinates: {
                  bsonType: "array",
                  minItems: 2,
                  maxItems: 2,
                  items: {
                    bsonType: "double",
                  },
                  description: "Must be an array of [longitude, latitude]",
                },
              },
            },
          },
        },
      },
    },
  },
});
// Índice único en email
db.users.createIndex({ email: 1 }, { unique: true });
// Índice geoespacial para buscar usuarios por ubicación (targets the nested field)
db.users.createIndex({ "direccion.ubicacion": "2dsphere" });

// 2) Colección "gyms"
db.createCollection("gyms", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "nombre",
        "direccion",
        "ubicacion",
        "precio",
        "actividades",
        "servicios",
        "averageRating",
        "reviewCount",
        "createdAt",
        "updatedAt",
      ],
      properties: {
        nombre: { bsonType: "string" },
        direccion: { bsonType: "string" },
        ubicacion: {
          bsonType: "object",
          required: ["type", "coordinates"],
          properties: {
            type: { enum: ["Point"] },
            coordinates: {
              bsonType: "array",
              minItems: 2,
              items: { bsonType: "double" },
            },
          },
        },
        precio: { bsonType: ["double", "int"] },
        actividades: { bsonType: "array", items: { bsonType: "string" } },
        servicios: { bsonType: "array", items: { bsonType: "string" } },
        ownerId: { bsonType: ["objectId", "null"] },
        averageRating: { bsonType: ["double", "int"] },
        reviewCount: { bsonType: "int" },
        createdAt: { bsonType: "date" },
        updatedAt: { bsonType: "date" },
        followers: { bsonType: "array", items: { bsonType: "objectId" } },
      },
    },
  },
});
// Índices para búsquedas
db.gyms.createIndex({ ubicacion: "2dsphere" });
db.gyms.createIndex({ ownerId: 1 });
db.gyms.createIndex({ averageRating: 1 });
db.gyms.createIndex({ actividades: 1 });
db.gyms.createIndex({ servicios: 1 });
db.gyms.createIndex({ createdAt: 1 });

// 3) Colección "reviews"
db.createCollection("reviews", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["gymId", "userId", "rating", "createdAt"],
      properties: {
        gymId: { bsonType: "objectId" },
        rating: { bsonType: ["double", "int"] },
        userId: { bsonType: "objectId" },
        comentario: { bsonType: "string" },
        createdAt: { bsonType: "date" },
      },
    },
  },
});
// Índices de búsqueda por referencias
db.reviews.createIndex({ gymId: 1 });
db.reviews.createIndex({ userId: 1 });
