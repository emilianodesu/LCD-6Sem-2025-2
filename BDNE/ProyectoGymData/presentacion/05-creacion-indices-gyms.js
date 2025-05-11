// Índices para búsquedas
db.gyms.createIndex({ ubicacion: "2dsphere" });
db.gyms.createIndex({ ownerId: 1 });
db.gyms.createIndex({ averageRating: 1 });
db.gyms.createIndex({ actividades: 1 });
db.gyms.createIndex({ servicios: 1 });
db.gyms.createIndex({ createdAt: 1 });
