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
