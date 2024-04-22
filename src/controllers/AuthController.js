const userRepository = require('../repositories/UserRepository');
const bcrypt = require('bcrypt');

class AuthController {
    async login(req, res) {
        const { email, senha } = req.body;
    
        try {
            const user = await userRepository.findUserByEmail(email);
    
            if (!user) {
                console.log('Usuário não encontrado');
                return res.status(401).json({ message: 'Usuário não encontrado' });
            }
            
            const senhaCorreta = await bcrypt.compare(senha, user.password);
            if (!senhaCorreta) {
                console.log('Senha inválida');
                return res.status(401).json({ message: 'Senha inválida' });
            }

            console.log('Login bem-sucedido');
            res.status(200).json({ message: 'Login bem-sucedido' });
        } catch (error) {
            console.error('Erro durante o login:', error);
            res.status(500).json({ message: 'Erro ao fazer login' });
        }        
    }
}

module.exports = new AuthController();
