"""
Login page assets and animations
Handles video backgrounds and creative effects
"""

import streamlit as st
import base64
from pathlib import Path

def get_video_background_css():
    """Get CSS for animated video background"""
    return """
    <style>
        /* Animated particles background */
        .particles-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -2;
            overflow: hidden;
        }
        
        .particle-float {
            position: absolute;
            width: 4px;
            height: 4px;
            background: #00d9ff;
            border-radius: 50%;
            opacity: 0.5;
            animation: float 20s infinite;
            filter: blur(0.5px);
        }
        
        .particle-float:nth-child(1) { left: 10%; top: 20%; animation-delay: 0s; }
        .particle-float:nth-child(2) { left: 20%; top: 50%; animation-delay: 2s; }
        .particle-float:nth-child(3) { left: 30%; top: 80%; animation-delay: 4s; }
        .particle-float:nth-child(4) { left: 50%; top: 10%; animation-delay: 6s; }
        .particle-float:nth-child(5) { left: 70%; top: 40%; animation-delay: 8s; }
        .particle-float:nth-child(6) { left: 80%; top: 70%; animation-delay: 10s; }
        .particle-float:nth-child(7) { left: 90%; top: 30%; animation-delay: 12s; }
        .particle-float:nth-child(8) { left: 15%; top: 60%; animation-delay: 14s; }
        .particle-float:nth-child(9) { left: 85%; top: 15%; animation-delay: 16s; }
        .particle-float:nth-child(10) { left: 40%; top: 90%; animation-delay: 18s; }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) translateX(0px); opacity: 0; }
            10% { opacity: 0.5; }
            50% { transform: translateY(-100px) translateX(50px); opacity: 0.8; }
            90% { opacity: 0.5; }
        }
        
        /* Pulsing glow effect */
        .glow-element {
            position: fixed;
            border-radius: 50%;
            filter: blur(40px);
            opacity: 0.2;
            z-index: -1;
        }
        
        .glow-cyan {
            width: 400px;
            height: 400px;
            background: #00d9ff;
            top: -150px;
            left: -150px;
            animation: moveGlow 15s ease-in-out infinite;
        }
        
        .glow-magenta {
            width: 350px;
            height: 350px;
            background: #d946ef;
            bottom: -100px;
            right: -100px;
            animation: moveGlow 20s ease-in-out infinite reverse;
        }
        
        .glow-teal {
            width: 300px;
            height: 300px;
            background: #00f5dd;
            top: 50%;
            right: 5%;
            animation: moveGlow 18s ease-in-out infinite;
        }
        
        @keyframes moveGlow {
            0%, 100% { transform: translate(0, 0); }
            33% { transform: translate(30px, -50px); }
            66% { transform: translate(-30px, 50px); }
        }
        
        /* Gradient mesh animation */
        .mesh-gradient {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -3;
            background: linear-gradient(45deg, #0a0e27 0%, #111829 25%, #0d1426 50%, #1a1f3a 75%, #0a0e27 100%);
            background-size: 400% 400%;
            animation: gradientMesh 15s ease infinite;
        }
        
        @keyframes gradientMesh {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Video background styling */
        .video-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            object-fit: cover;
            opacity: 0.15;
            filter: blur(3px) brightness(0.6);
        }
    </style>
    """

def show_animated_background():
    """Display animated background elements"""
    st.markdown(get_video_background_css(), unsafe_allow_html=True)
    
    # Create animated particles HTML
    particles_html = """
    <div class="mesh-gradient"></div>
    <div class="glow-element glow-cyan"></div>
    <div class="glow-element glow-magenta"></div>
    <div class="glow-element glow-teal"></div>
    <div class="particles-container">
    """
    
    # Add floating particles
    for i in range(10):
        particles_html += "<div class='particle-float'></div>"
    
    particles_html += "</div>"
    
    st.markdown(particles_html, unsafe_allow_html=True)

def create_sample_background_video():
    """
    Create a simple animated background video file
    Returns path to the video file
    """
    try:
        import numpy as np
        from PIL import Image, ImageDraw
        import tempfile
        import subprocess
        
        # Create a temporary directory
        temp_dir = Path(tempfile.gettempdir()) / "eda_assets"
        temp_dir.mkdir(exist_ok=True)
        
        video_path = temp_dir / "login_background.mp4"
        
        # If video already exists, return it
        if video_path.exists():
            return str(video_path)
        
        # Create frames for animation
        frames_dir = temp_dir / "frames"
        frames_dir.mkdir(exist_ok=True)
        
        # Generate 60 frames (2 seconds at 30fps)
        for frame_num in range(60):
            # Create image with gradient
            img = Image.new('RGB', (1920, 1080), color='#0a0e27')
            draw = ImageDraw.Draw(img, 'RGBA')
            
            # Create animated gradient
            progress = frame_num / 60
            
            # Draw gradient rectangles
            for i in range(0, 1920, 100):
                alpha = int(255 * (0.3 + 0.2 * np.sin(progress * 2 * np.pi + i / 500)))
                draw.rectangle(
                    [(i, 0), (i + 100, 1080)],
                    fill=(0, 217, 255, alpha)
                )
            
            # Draw circles (particles)
            for j in range(5):
                x = int(960 + 400 * np.cos(progress * 2 * np.pi + j))
                y = int(540 + 300 * np.sin(progress * 2 * np.pi + j))
                radius = 100
                draw.ellipse(
                    [(x - radius, y - radius), (x + radius, y + radius)],
                    fill=(217, 70, 239, int(100 * (0.3 + 0.2 * np.sin(progress * 2 * np.pi))))
                )
            
            img.save(frames_dir / f"frame_{frame_num:03d}.png")
        
        # Combine frames into video using ffmpeg if available
        try:
            subprocess.run([
                'ffmpeg', '-y', '-framerate', '30',
                '-i', str(frames_dir / 'frame_%03d.png'),
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                str(video_path)
            ], capture_output=True, timeout=30)
            
            return str(video_path)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # If ffmpeg fails or not available, return None
            return None
            
    except Exception as e:
        print(f"Error creating background video: {e}")
        return None

def get_login_page_html_template():
    """Get complete HTML template for creative login page"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Auto EDA Studio Pro - Login</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0a0e27 0%, #111829 50%, #0d1426 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
            }
            
            .background {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: -1;
            }
            
            .mesh-gradient {
                width: 100%;
                height: 100%;
                background: linear-gradient(45deg, #0a0e27 0%, #111829 25%, #0d1426 50%, #1a1f3a 75%, #0a0e27 100%);
                background-size: 400% 400%;
                animation: gradientMesh 15s ease infinite;
            }
            
            @keyframes gradientMesh {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            .glow {
                position: fixed;
                border-radius: 50%;
                filter: blur(40px);
                opacity: 0.2;
            }
            
            .glow-1 {
                width: 400px;
                height: 400px;
                background: #00d9ff;
                top: -150px;
                left: -150px;
                animation: moveGlow 15s ease-in-out infinite;
            }
            
            .glow-2 {
                width: 350px;
                height: 350px;
                background: #d946ef;
                bottom: -100px;
                right: -100px;
                animation: moveGlow 20s ease-in-out infinite reverse;
            }
            
            @keyframes moveGlow {
                0%, 100% { transform: translate(0, 0); }
                50% { transform: translate(30px, -50px); }
            }
            
            .container {
                position: relative;
                z-index: 10;
                max-width: 450px;
                width: 90%;
            }
            
            .login-card {
                backdrop-filter: blur(20px);
                background: rgba(17, 24, 41, 0.85);
                border: 2px solid rgba(0, 217, 255, 0.3);
                border-radius: 20px;
                padding: 60px 50px;
                box-shadow: 
                    0 8px 32px rgba(0, 217, 255, 0.2),
                    inset 0 0 60px rgba(0, 217, 255, 0.05);
                animation: slideInUp 0.8s ease-out;
            }
            
            @keyframes slideInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            
            .title {
                font-size: 2.5em;
                font-weight: 800;
                background: linear-gradient(135deg, #00d9ff 0%, #00f5dd 50%, #d946ef 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 10px;
                letter-spacing: 1px;
            }
            
            .subtitle {
                font-size: 0.95em;
                color: #a0aec0;
                letter-spacing: 2px;
                text-transform: uppercase;
            }
            
            .form-group {
                margin-bottom: 25px;
            }
            
            .label {
                display: block;
                margin-bottom: 10px;
                font-size: 0.9em;
                font-weight: 600;
                color: #00d9ff;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            input {
                width: 100%;
                padding: 16px 20px;
                background: rgba(10, 14, 39, 0.5);
                border: 2px solid rgba(0, 217, 255, 0.2);
                border-radius: 12px;
                color: #ffffff;
                font-size: 1em;
                transition: all 0.3s ease;
            }
            
            input:focus {
                border-color: #00d9ff;
                background: rgba(10, 14, 39, 0.8);
                box-shadow: 0 0 25px rgba(0, 217, 255, 0.4);
                outline: none;
            }
            
            .button-group {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
                margin-top: 30px;
            }
            
            button {
                padding: 14px 28px;
                border: none;
                border-radius: 10px;
                font-weight: 700;
                font-size: 1em;
                cursor: pointer;
                text-transform: uppercase;
                letter-spacing: 1px;
                transition: all 0.3s ease;
            }
            
            .login-btn {
                background: linear-gradient(135deg, #00d9ff 0%, #00f5dd 100%);
                color: #0a0e27;
                box-shadow: 0 0 30px rgba(0, 217, 255, 0.3);
            }
            
            .login-btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 0 50px rgba(0, 217, 255, 0.6);
            }
            
            .demo-btn {
                background: rgba(217, 70, 239, 0.2);
                border: 2px solid rgba(217, 70, 239, 0.5);
                color: #d946ef;
            }
            
            .demo-btn:hover {
                background: rgba(217, 70, 239, 0.4);
                transform: translateY(-3px);
                box-shadow: 0 0 30px rgba(217, 70, 239, 0.4);
            }
            
            .footer {
                text-align: center;
                margin-top: 35px;
                padding-top: 25px;
                border-top: 1px solid rgba(0, 217, 255, 0.1);
                font-size: 0.85em;
                color: #718096;
            }
        </style>
    </head>
    <body>
        <div class="background">
            <div class="mesh-gradient"></div>
            <div class="glow glow-1"></div>
            <div class="glow glow-2"></div>
        </div>
        
        <div class="container">
            <div class="login-card">
                <div class="header">
                    <div class="title">🔐 AUTO EDA</div>
                    <div class="subtitle">Studio Pro Authentication</div>
                </div>
                
                <form id="loginForm">
                    <div class="form-group">
                        <label class="label">👤 Username</label>
                        <input type="text" id="username" placeholder="Enter your username" required>
                    </div>
                    
                    <div class="form-group">
                        <label class="label">🔑 Password</label>
                        <input type="password" id="password" placeholder="Enter your password" required>
                    </div>
                    
                    <div class="button-group">
                        <button type="submit" class="login-btn">🚀 LOGIN</button>
                        <button type="button" class="demo-btn" onclick="showDemo()">📋 DEMO</button>
                    </div>
                </form>
                
                <div class="footer">
                    <p>🛡️ <strong>Secure Login</strong> | 📊 <strong>Advanced Analytics</strong> | 📄 <strong>PDF Export</strong></p>
                    <p style="margin-top: 10px; font-size: 0.8em;">Auto EDA Studio Pro v2.0 | Enterprise Analytics Platform</p>
                </div>
            </div>
        </div>
        
        <script>
            function showDemo() {
                alert('Demo Accounts:\\n\\nAdmin:\\nUsername: admin\\nPassword: admin123\\n\\nUser:\\nUsername: user\\nPassword: user123');
            }
            
            document.getElementById('loginForm').addEventListener('submit', function(e) {
                e.preventDefault();
                console.log('Login attempt');
            });
        </script>
    </body>
    </html>
    """
