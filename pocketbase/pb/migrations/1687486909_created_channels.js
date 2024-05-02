migrate((db) => {
  const collection = new Collection({
    "id": "viyn8674i5glpcj",
    "created": "2023-06-23 02:21:49.034Z",
    "updated": "2023-06-23 02:21:49.034Z",
    "name": "channels",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "yq5k5n3j",
        "name": "channel_id",
        "type": "number",
        "required": false,
        "unique": false,
        "options": {
          "min": null,
          "max": null
        }
      },
      {
        "system": false,
        "id": "g6jltnii",
        "name": "mangas",
        "type": "relation",
        "required": false,
        "unique": false,
        "options": {
          "collectionId": "6mexouxnd1arbn1",
          "cascadeDelete": false,
          "minSelect": null,
          "maxSelect": null,
          "displayFields": []
        }
      }
    ],
    "indexes": [
      "CREATE UNIQUE INDEX `idx_DZk5b9E` ON `channels` (`channel_id`)"
    ],
    "listRule": "",
    "viewRule": "",
    "createRule": "",
    "updateRule": "",
    "deleteRule": "",
    "options": {}
  });

  return Dao(db).saveCollection(collection);
}, (db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("viyn8674i5glpcj");

  return dao.deleteCollection(collection);
})
