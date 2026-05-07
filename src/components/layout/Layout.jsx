import React from 'react';
import { Outlet, useLocation, useNavigate } from 'react-router-dom';

const Layout = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  const getActiveTab = () => {
    if (location.pathname.includes('/importer')) return 'importer';
    if (location.pathname.includes('/deals')) return 'deals';
    if (location.pathname.includes('/parser')) return 'parser';
    return 'importer'; 
  };
  
  const activeTab = getActiveTab();
  
  const handleTabClick = (tab) => {
    navigate(`/${tab}`);
  };

  return (
    <div className="app-container">
      {/* Боковая панель */}
      <div className="sidebar">
        <div className="sidebar-header">
          <h2>Bitrix24 Tools</h2>
          <p className="sidebar-subtitle">Инструменты для работы</p>
        </div>
        
        <nav className="sidebar-nav">
          <button
            className={`nav-button ${activeTab === 'importer' ? 'active' : ''}`}
            onClick={() => handleTabClick('importer')}
          >
            <span className="nav-text">Импорт данных</span>
            {activeTab === 'importer' && <div className="active-indicator"></div>}
          </button>

          <button
            className={`nav-button ${activeTab === 'deals' ? 'active' : ''}`}
            onClick={() => handleTabClick('deals')}
          >
            <span className="nav-text">Импорт сделок</span>
            {activeTab === 'deals' && <div className="active-indicator"></div>}
          </button>
          
          <button
            className={`nav-button ${activeTab === 'parser' ? 'active' : ''}`}
            onClick={() => handleTabClick('parser')}
          >
            <span className="nav-text">Парсер</span>
            {activeTab === 'parser' && <div className="active-indicator"></div>}
          </button>
        </nav>
      </div>

      <div className="main-content">
        <header className="main-header">
          <div className="header-left">
            <h1>
              {activeTab === 'importer' ? 'Импорт в смарт-процессы' : 'Парсер данных'}
            </h1>
          </div>
        </header>

        <div className="content-area">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default Layout;