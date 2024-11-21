import React from 'react';
import styles from './SignupForm.module.css';
import { Link } from 'react-router-dom';
import { SocialSignupButton } from './SocialSignupButton';
import { InputField } from './InputField';

export const SignupForm: React.FC = () => {
  const socialButtons = [
    { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/6c25a14c57def4cfc2bb01316fc7a70690f25da300dfdf3ea36e083cd2d82ea2?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', text: 'Signup with Facebook', variant: 'facebook' },
    { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/6658a138975c44bb4d019120bf7b03debbd334555acb7fe26d08e5215b665bc6?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', text: 'Signup with Google', variant: 'google' },
    { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/d2de2d44977ad52745b9e1e61d88be5a38f01c7510fc3ffeacd387737ba8f180?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', text: 'Signup with X', variant: 'x' }
  ] as const;

  return (
    <main className={styles.container}>
      <section className={styles.formSection}>
        <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/8c1450cd16cbcb30df27ad352a6e94379fabf80b38f87f9d4db1aa024485de6e?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9" alt="" className={styles.backgroundImage} />
        
        <form className={styles.formWrapper}>
          <h1 className={styles.title}>Create an account</h1>
          <p className={styles.subtitle}>Connect with your friends today!</p>
          <p className={styles.subtitleArabic}>اعمل فورمتك النهارده</p>

          <InputField placeholder="Enter Your Username" />
          <InputField placeholder="Enter Your Email" type="email" />
          <InputField placeholder="Enter Your Phone Number" type="tel" />
          <InputField 
            placeholder="Enter Your Password" 
            type="password"
            icon="https://cdn.builder.io/api/v1/image/assets/TEMP/482a3c01cbff113ec02eb181752319c28b143aad3dd3547789a587c4e45bbfe3?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9"
          />

          <button type="submit" className={styles.submitButton}>
            Sign Up
          </button>

          <div className={styles.divider}>
            <span className={styles.dividerLine} />
            <span className={styles.dividerText}>Or With</span>
            <span className={styles.dividerLine} />
          </div>

          {socialButtons.map((button) => (
            <SocialSignupButton key={button.text} {...button} />
          ))}

          <footer className={styles.footer}>
            <span>Already have an account? </span>
            <Link to="/" className={styles.loginLink}>Login</Link>
          </footer>
        </form>
      </section>
    </main>
  );
};
