import React from 'react';
import SortableTable from './SortableTable';
import itemsData from './data.json';
import { Item } from './types';

const App: React.FC = () => {
  const items: Item[] = itemsData;

  return (
    <div>
      <h1><img src="https://leetcode.com/_next/static/images/logo-dark-c96c407d175e36c81e236fcfdd682a0b.png" alt="" />LeetCode Leaderboard</h1>
      <SortableTable data={items} />
    </div>
  );
};

export default App;
