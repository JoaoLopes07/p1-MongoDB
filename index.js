const express = require('express');
const mongoose = require('mongoose');
const authRoutes = require('./src/routes/authRoutes');
const User = require('./src/models/User');
const path = require('path')

const app = express();

app.use(express.json());

// Conecta ao MongoDB
mongoose.connect('mongodb+srv://ifsjoao1234:jv070404@cluster0.lsn7yhy.mongodb.net/', {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => {
  console.log('Conectado ao MongoDB');
}).catch(err => {
  console.error('Erro ao conectar no MongoDB', err);
  process.exit(1);
});

app.get('/',(req,res)=>{
  res.sendFile(path.join(__dirname,'src', 'views','logar.html'));
});

// Rota para lidar com o login
app.post('/auth/login', async (req, res) => {
  const { email, senha } = req.body;
  try {
      // Verificar se o email corresponde a um usuário no banco de dados
      const user = await User.findOne({ email });

      // Verificar se o usuário existe e se a senha está correta
      if (user && user.password === senha) {
          // Se as credenciais estiverem corretas, enviar uma resposta de sucesso
          res.json({ success: true, message: 'Login bem-sucedido' });
      } else {
          // Se as credenciais estiverem incorretas, enviar uma resposta de erro
          res.status(401).json({ success: false, message: 'Credenciais inválidas' });
      }
  } catch (error) {
      console.error('Erro ao fazer login:', error);
      res.status(500).json({ success: false, message: 'Erro ao fazer login' });
  }
});


// Rotas de autenticação
app.use('/auth', authRoutes);

app.use('/api/auth', authRoutes);

app.post('/api/usuarios', async (req, res) => {
  const { username, password, email } = req.body;
  try {
    const novoUsuario = new User({
      username: username,
      password: password,
      email: email
    });

    await novoUsuario.save();

    res.status(201).json({ message: 'Usuário adicionado com sucesso' });
  } catch (error) {
    console.error('Erro ao adicionar usuário:', error);
    res.status(500).json({ message: 'Erro ao adicionar usuário' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server está rodando na porta ${PORT}`);
});