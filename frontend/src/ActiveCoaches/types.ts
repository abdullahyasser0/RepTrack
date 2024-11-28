
  export interface SidebarItemProps {
    icon: string;
    label: string;
    isActive?: boolean;
    onClick?: () => void;
  }
  
  export interface CoachItemProps {
    name: string;
    id: string;
    contact: string;
    expirationDate: string;
  }
  
  export interface PaginationProps {
    onPrevious: () => void;
    onNext: () => void;
  }
  
  export interface HeaderProps {
    adminName: string;
    adminEmail: string;
    profileImage: string;
  }
  
  export interface SearchBarProps {
    onSearch: (query: string) => void;
  }

  export interface MemberRowProps {
    name: string;
    memberId: string;
    dateEnrolled: string;
    dateExpiration: string;
  }

  export interface AdminProfileProps {
    name: string;
    email: string;
    avatar: string;
  }