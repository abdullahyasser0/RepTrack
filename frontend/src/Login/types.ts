export interface SocialLoginButtonProps {
    icon: string;
    text: string;
    variant: 'primary' | 'secondary' | 'dark';
    onClick?: () => void;
  }
  
  export interface InputFieldProps {
    label: string;
    type?: string;
    value?: string;
    icon?: string;
    onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  }