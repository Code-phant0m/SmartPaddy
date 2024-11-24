/* eslint-disable linebreak-style */
const { regisUserHandler, loginUserHandler } = require('./handler');

const routes = [
  {
    method: 'POST',
    path: '/register',
    handler: regisUserHandler,
  },
  {
    method: 'POST',
    path: '/login',
    handler: loginUserHandler,
  },
];

module.exports = routes;