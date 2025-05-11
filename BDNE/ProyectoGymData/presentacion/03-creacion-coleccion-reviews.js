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
