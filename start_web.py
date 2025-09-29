#!/usr/bin/env python3
"""
Script para iniciar a interface web do Instagram Automation
"""

import os
import sys
import webbrowser
import time
from threading import Timer

def open_browser():
    """Abre o navegador após 2 segundos"""
    webbrowser.open('http://localhost:5000')

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                INSTAGRAM AUTOMATION WEB                     ║
    ║                    Interface Web                            ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    print("🚀 Iniciando servidor web...")
    print("📱 A interface será aberta automaticamente no navegador")
    print("🌐 URL: http://localhost:5000")
    print("🛑 Para parar: Ctrl+C")
    print()
    
    # Abrir navegador após 2 segundos
    Timer(2.0, open_browser).start()
    
    # Importar e executar a aplicação web
    try:
        # Compatibilidade para Python 3.12+/3.13: alguns pacotes ainda importam 'distutils'
        import sys as _sys, importlib as _importlib, subprocess as _subprocess
        try:
            import distutils  # type: ignore
        except ModuleNotFoundError:
            try:
                import setuptools._distutils as _distutils  # type: ignore
                _sys.modules['distutils'] = _distutils
            except Exception:
                try:
                    # garantir setuptools instalado
                    _subprocess.check_call([_sys.executable, '-m', 'pip', 'install', '--quiet', 'setuptools'])
                    import setuptools._distutils as _distutils  # type: ignore
                    _sys.modules['distutils'] = _distutils
                except Exception:
                    pass
        
        from web_app import app, db, User
        # criar banco e um usuário admin default se não existir
        with app.app_context():
            db.create_all()
            if not User.query.filter_by(username='admin').first():
                db.session.add(User(username='admin', password='admin'))
                db.session.commit()
                print("👤 Usuário padrão criado: admin / admin")
        app.run(debug=False, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"❌ Erro ao importar web_app: {e}")
        print("💡 Certifique-se de que todos os arquivos estão no diretório correto")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Servidor web parado pelo usuário!")
        sys.exit(0)
