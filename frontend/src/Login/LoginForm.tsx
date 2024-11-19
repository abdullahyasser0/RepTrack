import styles from './LoginForm.module.css';
import { SocialLoginButton } from './SocialLoginButton';
import { InputField } from './InputField';

export const LoginForm: React.FC = () => {
  const socialLogins: { icon: string; text: string; variant: "primary" | "secondary" | "dark"; }[] = [
    { 
      icon: "https://cdn.builder.io/api/v1/image/assets/TEMP/a6e6c2ad92229ef5ea56f0d1aaab0f8026348d8244ea079c79a1ba13354953e7?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9", 
      text: "Login with Facebook", 
      variant: 'primary' 
    },
    { 
      icon: "https://cdn.builder.io/api/v1/image/assets/TEMP/ae4273c5a573ab7930804958d0b59c0432b59af31c59f89db1b79b981a4d58ab?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9", 
      text: "Login with Google", 
      variant: 'secondary' 
    },
    { 
      icon: "https://cdn.builder.io/api/v1/image/assets/TEMP/492fe172f68991359a95a012c4201d3fdcae5ce38b90ceca5597e8940702b598?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9", 
      text: "Signup with X", 
      variant: 'dark' 
    }
  ];

  return (
    <main className={styles.container}>
      <section className={styles.formSection}>
        <img loading="lazy" src="https://cdn.builder.io/api/v1/image/assets/TEMP/73859a4080c54497641fa264d99c94f756e5713418b21e17db00286aa16c3403?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9" alt="" className={styles.backgroundImage} />
        
        <form className={styles.loginForm}>
          <h1 className={styles.welcomeText}>Hi, Welcome Back! 👋</h1>
          
          <InputField label="Email" value="example@gmail.com" />
          <InputField 
            label="Password" 
            type="password" 
            value="Enter Your Password"
            icon="https://cdn.builder.io/api/v1/image/assets/TEMP/576cce65a6f5a54005d0c024121ec174dd368897178c9898196255f404df8f5f?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9"
          />

          <div className={styles.formOptions}>
            <label className={styles.rememberMe}>
              <input type="checkbox" className={styles.checkbox} />
              <span>Remember Me</span>
            </label>
            <button type="button" className={styles.forgotPassword}>
              Forgot Password?
            </button>
          </div>

          <button type="submit" className={styles.loginButton}>
            Login
          </button>

          <div className={styles.divider}>
            <span className={styles.dividerText}>Or With</span>
            <hr className={styles.dividerLine} />
          </div>

          {socialLogins.map((login, index) => (
            <SocialLoginButton key={index} {...login} />
          ))}

          <footer className={styles.formFooter}>
            <span>Don't have an account?</span>
            <button type="button" className={styles.signupLink}>Sign Up</button>
          </footer>
        </form>
      </section>
    </main>
  );
};
