import React from 'react';
import { SearchBarProps } from './types';
import styles from './MemberDashboard.module.css';

export const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  return (
    <div className={styles.searchContainer}>
      <input
        type="text"
        className={styles.searchInput}
        placeholder="Search"
        onChange={(e) => onSearch(e.target.value)}
        aria-label="Search members"
      />
      <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/7ce633642c613447bfb2c3158c5a686e652b276f026cd3df0f31666cebaa94b3?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9" alt="" className={styles.searchIcon} />
    </div>
  );
};