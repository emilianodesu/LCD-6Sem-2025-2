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
