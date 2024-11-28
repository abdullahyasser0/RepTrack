import React from 'react';
import { SidebarItemProps } from './types';
import styles from './AdminDashboard.module.css';



export const SidebarItem: React.FC<SidebarItemProps> = ({ icon, label, isActive, onClick }) => {
  const itemClass = isActive ? styles.sidebarItemActive : styles.sidebarItem;
  
  return (
    <div className={itemClass} onClick={onClick} role="button" tabIndex={0}>
      <img src={icon} alt="" className={styles.sidebarIcon} />
      <span className={styles.sidebarLabel}>{label}</span>
    </div>
  );
};