export interface SidebarItemProps {
    icon: string;
    label: string;
    isActive?: boolean;
    onClick?: () => void;
  }
  
  export interface ButtonProps {
    variant: 'primary' | 'secondary';
    children: React.ReactNode;
    onClick?: () => void;
  }
  
  export interface ProfileFormProps {
    onSubmit: (data: ProfileFormData) => void;
    initialData?: ProfileFormData;
  }
  
  export interface ProfileFormData {
    username: string;
    contactNo: string;
    emailAddress: string;
  }
  
  export interface PasswordFormData {
    currentPassword: string;
    newPassword: string;
    retypePassword: string;
  }