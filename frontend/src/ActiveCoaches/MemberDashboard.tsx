import React from 'react';
import { SidebarItem } from './Sidebarltem';
import { MemberRow } from './MemberRow';
import { SearchBar } from './SearchBar';
import { AdminProfile } from './AdminProfile';
import styles from './MemberDashboard.module.css';

const sidebarItems = [
  { icon: "https://cdn.builder.io/api/v1/image/assets/TEMP/e5b1e5633d6552fb186cda6d7b018a7309401bc6476ac546ea456b7a53218ee2?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9", label: "Dashboard" },
  { icon: "https://cdn.builder.io/api/v1/image/assets/TEMP/828bdaed89fa2b3dca335bb36a4b59034bef3115f1d8f994aed35376edd9ea27?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9", label: "Admin Profile" },
  { icon: "https://cdn.builder.io/api/v1/image/assets/TEMP/91ea35adcf4c15f7de9e46d4e8a684843614d81b43486c871c2dc4a24bb1577c?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9", label: "Registration" },
  { icon: "https://cdn.builder.io/api/v1/image/assets/TEMP/2d0b23297916b9ea76e0027f5c6f1ab73bf4b11444b917fbc4b5bf41cea7f320?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9", label: "Plan" },
  { icon: "https://cdn.builder.io/api/v1/image/assets/TEMP/4069869669541f912d375e2daa0017d83c9b4f3ef7fbef7c22bf163e08e2995a?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9", label: "Payment" },
  { icon: "https://cdn.builder.io/api/v1/image/assets/TEMP/6e37d24962b4f6fa75b6e2ef7bdc7c966c7846fb1b069a9f8d2de6f3b9021bb1?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9", label: "Inventory" },
  { icon: "https://cdn.builder.io/api/v1/image/assets/TEMP/98c5d1f68dbbee6f5c4749856e73c836b83f8189be1a65222be823f2732cd5b4?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9", label: "View Members", isActive: true },
  { icon: "https://cdn.builder.io/api/v1/image/assets/TEMP/285c0da56596654a53b4f73089a93478c8405b5c7755f6096c2eb2f748089edb?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9", label: "Coaches" },
  { icon: "https://cdn.builder.io/api/v1/image/assets/TEMP/d002c6948a89f562362781c3b8ad4fa9b23e68bb8ebb61267f75552840217a47?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9", label: "Report" },
  { icon: "https://cdn.builder.io/api/v1/image/assets/TEMP/38a1d2c0b187afe65c69c5cab793a7e26a5ca2bbd6d74012f68c6564a621af04?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9", label: "Logout" }
];

const members = [
  { name: "Member 1", memberId: "SFM2301N1", dateEnrolled: "Jan 11", dateExpiration: "Feb 11" },
  { name: "Member 2", memberId: "SFM2301N2", dateEnrolled: "Jan 11", dateExpiration: "Feb 11" },
  { name: "Member 3", memberId: "SFM2301N3", dateEnrolled: "Jan 11", dateExpiration: "Feb 11" },
  { name: "Member 4", memberId: "SFM2301N4", dateEnrolled: "Jan 11", dateExpiration: "Feb 11" }
];

export const MemberDashboard: React.FC = () => {
  const handleSearch = (query: string) => {
    // Implement search functionality
  };

  return (
    <div className={styles.dashboard}>
      <div className={styles.sidebar}>
        <AdminProfile
          name="Administrator Name"
          email="juan.delacruz@gmail.com"
          avatar="https://cdn.builder.io/api/v1/image/assets/TEMP/7477ef3815498d2ce9eeb802bff93c8fa845d2c34cb1bce39392217eef551f11?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9"
        />
        {sidebarItems.map((item, index) => (
          <SidebarItem key={index} {...item} />
        ))}
      </div>
      
      <div className={styles.mainContent}>
        <div className={styles.header}>
          <div className={styles.headerTitle}>
            <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/ea58de615482b6fbb8bdb9990c83b114973529133782fdc8e652424da510dbaf?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9" alt="" className={styles.headerIcon} />
            <h1 className={styles.headerText}>Active Members</h1>
          </div>
          <div className={styles.headerActions}>
            <span>Feedback</span>
            <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/acc53ef920e776438bea3daa983751f0134e7952ebb015f4d5dc6033b8fc0ce6?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9" alt="" className={styles.feedbackIcon} />
          </div>
        </div>

        <div className={styles.membersSection}>
          <div className={styles.membersHeader}>
            <h2 className={styles.membersTitle}>Gym Members</h2>
            <SearchBar onSearch={handleSearch} />
          </div>

          <div className={styles.membersTable}>
            <div className={styles.tableHeader}>
              <div>Name</div>
              <div>Member ID</div>
              <div>Date Enrolled</div>
              <div>Date Expiration</div>
              <div>Actions</div>
            </div>
            
            {members.map((member, index) => (
              <MemberRow key={index} {...member} />
            ))}
          </div>

          <div className={styles.pagination}>
            <button className={styles.paginationButton}>Previous</button>
            <button className={styles.paginationButton}>Next</button>
          </div>
        </div>
      </div>
    </div>
  );
};