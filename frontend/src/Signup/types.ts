export interface SocialSignupButtonProps {
    icon: string;
    text: string;
    variant: 'facebook' | 'google' | 'x';
    onClick?: () => void;
  }
  
  export interface InputFieldProps {
    placeholder: string;
    type?: string;
    icon?: string;
  }