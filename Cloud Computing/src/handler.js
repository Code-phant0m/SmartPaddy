/* eslint-disable linebreak-style */
const { nanoid } = require('nanoid');
const users = require('./users');

const regisUserHandler = (request, h) => {
  const { name, email, password } = request.payload;

  const token = nanoid(16);

  const newUser = {
    token,
    name,
    email,
    password
  };

  if (!name || !email || !password){
    const response = h.response({
      status: 'fail',
      message: 'Mohon isi seluruh data'
    });
    response.code(400);
    return response;
  }

  const existingUser = users.find((user) => user.email === email);
  if (existingUser) {
    const response = h.response({
      status: 'fail',
      message: 'Email sudah terdaftar'
    });
    response.code(400);
    return response;
  }

  users.push(newUser);

  const response = h.response({
    status: 'success',
    message: 'User berhasil ditambahkan',
    user: {
      token,
      name,
      email,
      password
    }
  });
  response.code(201);
  return response;
};

const loginUserHandler = (request, h) => {
  const { email, password } = request.payload;

  if (!email || !password) {
    const response = h.response({
      status: 'fail',
      message: 'Mohon isi email dan password'
    });
    response.code(400);
    return response;
  }

  const user = users.find((user) => user.email === email);

  if (!user || user.password !== password) {
    const response = h.response({
      status: 'fail',
      message: 'Email atau password salah'
    });
    response.code(401);
    return response;
  }

  const response = h.response({
    status: 'success',
    token: user.token,
    message: 'Selamat datang di SmartPaddy'
  });
  response.code(200);
  return response;
};


module.exports = { regisUserHandler, loginUserHandler };