// ROUTES
//  /server/:id/subscribe/:manga_id
//  body:
//    roles (to notify)
//  If manga_id not track by the app (not present in the manga table)
//    track it using the manga_id
//      make a request to get the manga info using the API (name, chapters)
//      create the row in the db using the infos
//  If tracked
//    create a joined row between the manga row and the server row
//      add the roles to notify (if any)
