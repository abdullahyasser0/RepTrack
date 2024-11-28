import React from 'react';
import { Header } from './Header';
import { SidebarItem } from './Sidebarltem';
import { CoachItem } from './Coachltem';
import { Pagination } from './Pagination';
import styles from './AdminDashboard.module.css';

const sidebarItems = [
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/e5b1e5633d6552fb186cda6d7b018a7309401bc6476ac546ea456b7a53218ee2?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'Dashboard' },
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/cbff539d3332e2857af5b323dbeb00a14a41ed398999bfd9808de8cdc1134d8c?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'Admin Profile' },
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/924cd441e1c0088fd992bf81e391ca48c62c1aed5c4175f8e7e0017d16337df3?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'Registration' },
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/a1e5c6616e1490e1e4c3d0755c05853eeee4789686c4ce528ce73d1c1f04af5a?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'Plan' },
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/bf2141a49a8af6d897af6f3d589b2de8eed81be37dd998dff36157d5d85fc576?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'Payment' },
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/f4bc3dead8c4862b4cd10c9d0eae9cd8f144ba9225ceab2e5f592f058254faca?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'Inventory' },
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/86184e038a7647fc42fa716208a0f37c701e13b2b4ed3f3d3bb780f80a2e6972?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'View Members' },
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/03119b4ce916fd493596a245d2b2548910907c2bff45b9119ffdf0482ecf13f8?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'Coaches', isActive: true },
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/e7e1fbdd3b6a9d09d001c80401b55378ebb2492cc13a1b89102777dbb4045713?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'Report' },
  { icon: 'https://cdn.builder.io/api/v1/image/assets/TEMP/f28fd7f20fa2518cf9b3c5aa375d07b3a5f2afc60eeb96d9f56bfc2ee21cd6c2?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9', label: 'Logout' }
];

const coaches = [
  { name: 'Coach 1', id: 'SFM2301N1', contact: '555-0123', expirationDate: 'Jan 11' },
  { name: 'Coach 2', id: 'SFM2301N2', contact: '555-0124', expirationDate: 'Feb 11' },
  { name: 'Coach 3', id: 'SFM2301N3', contact: '555-0125', expirationDate: 'Feb 11' }
];

export const AdminDashboard: React.FC = () => {
  return (
    <div className={styles.dashboard}>
      <div className={styles.container}>
        <aside className={styles.sidebar}>
          <Header
            adminName="Administrator Name"
            adminEmail="juan.delacruz@gmail.com"
            profileImage="https://cdn.builder.io/api/v1/image/assets/TEMP/82939e4fdec79a94d1447884de3fc2e2a65da2e919fc18dcf03e138c27eb9bc3?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9"
          />
          {sidebarItems.map((item, index) => (
            <SidebarItem key={index} {...item} />
          ))}
        </aside>
        
        <main className={styles.mainContent}>
          <div className={styles.topBar}>
            <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/ea58de615482b6fbb8bdb9990c83b114973529133782fdc8e652424da510dbaf?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9" alt="" className={styles.logo} />
            <div className={styles.feedbackSection}>
              <span>Feedback</span>
              <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/88f76617d1f7973f3a5fc6350dbeb11f5a5f56fea520051ecd009a3792223ba3?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9" alt="" className={styles.feedbackIcon} />
            </div>
          </div>

          <section className={styles.coachesSection}>
            <h1 className={styles.sectionTitle}>Active Coaches</h1>
            <button className={styles.addCoachButton}>Add Coach</button>
            
            <div className={styles.coachesContainer}>
              <div className={styles.coachesHeader}>
                <div className={styles.headerControls}>
                  <div className={styles.entityControl}>
                    <span>Show Entities</span>
                    <div className={styles.entitySelector}>
                      <span>10</span>
                      <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/73f3d1e57ab5d61e382a9ad9012a3e32f2a801d5e397a39b1abb5ca23cc41a60?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9" alt="" className={styles.dropdownIcon} />
                    </div>
                  </div>
                  <div className={styles.searchBox}>
                    <span>Search</span>
                    <img src="https://cdn.builder.io/api/v1/image/assets/TEMP/952c0e6f23cb3974c6c29f11445f4fc4a9028dbfa70fbf1adf498369f43de212?placeholderIfAbsent=true&apiKey=e9d236d8c0c94057ac283d5229bb03b9" alt="" className={styles.searchIcon} />
                  </div>
                </div>
              </div>

              <div className={styles.coachList}>
                {coaches.map((coach, index) => (
                  <CoachItem key={index} {...coach} />
                ))}
              </div>

              <Pagination 
                onPrevious={() => console.log('Previous')}
                onNext={() => console.log('Next')}
              />
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};