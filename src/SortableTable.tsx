import React, { useState } from 'react';
import { Item } from './types';

type SortKey = keyof Item;
type SortOrder = 'asc' | 'desc';

interface Props {
  data: Item[];
}

const SortableTable: React.FC<Props> = ({ data }) => {
  const [sortKey, setSortKey] = useState<SortKey>('username');
  const [sortOrder, setSortOrder] = useState<SortOrder>('asc');

  const handleSort = (key: SortKey) => {
    if (key === sortKey) {
      setSortOrder(prev => (prev === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortKey(key);
      setSortOrder('asc');
    }
  };

  const sortedData = [...data].sort((a, b) => {
    const aVal = a[sortKey];
    const bVal = b[sortKey];
    if (aVal < bVal) return sortOrder === 'asc' ? -1 : 1;
    if (aVal > bVal) return sortOrder === 'asc' ? 1 : -1;
    return 0;
  });

  return (
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th> Rank <button onClick={() => handleSort('ranking')} style={{width: "5px", height: "10px", fontSize: "20px", display:"flex", justifyContent: "center", alignItems: "center"}}>↑↓</button></th>
          <th> Country <button onClick={() => handleSort('countryName')} style={{width: "5px", height: "10px", fontSize: "20px", display:"flex", justifyContent: "center", alignItems: "center"}}>↑↓</button></th>
          <th> Username <button onClick={() => handleSort('username')} style={{width: "5px", height: "10px", fontSize: "20px", display:"flex", justifyContent: "center", alignItems: "center"}}>↑↓</button></th>
          <th> Solved <button onClick={() => handleSort('totalProblemsSolved')} style={{width: "5px", height: "10px", fontSize: "20px", display:"flex", justifyContent: "center", alignItems: "center"}}>↑↓</button></th>
          <th> Easy <button onClick={() => handleSort('easySolved')} style={{width: "5px", height: "10px", fontSize: "20px", display:"flex", justifyContent: "center", alignItems: "center"}}>↑↓</button></th>
          <th> Medium <button onClick={() => handleSort('mediumSolved')} style={{width: "5px", height: "10px", fontSize: "20px", display:"flex", justifyContent: "center", alignItems: "center"}}>↑↓</button></th>
          <th> Hard <button onClick={() => handleSort('hardSolved')} style={{width: "5px", height: "10px", fontSize: "20px", display:"flex", justifyContent: "center", alignItems: "center"}}>↑↓</button></th>
          <th> AC Rate <button onClick={() => handleSort('acceptanceRate')} style={{width: "5px", height: "10px", fontSize: "20px", display:"flex", justifyContent: "center", alignItems: "center"}}>↑↓</button></th>
          <th> Submissions <button onClick={() => handleSort('submissions')} style={{width: "5px", height: "10px", fontSize: "20px", display:"flex", justifyContent: "center", alignItems: "center"}}>↑↓</button></th>
          <th> Streak <button onClick={() => handleSort('currentStreak')} style={{width: "5px", height: "10px", fontSize: "20px", display:"flex", justifyContent: "center", alignItems: "center"}}>↑↓</button></th>
          <th> Highest Streak <button onClick={() => handleSort('maxStreak')} style={{width: "5px", height: "10px", fontSize: "20px", display:"flex", justifyContent: "center", alignItems: "center"}}>↑↓</button></th>
          <th> Submit Days <button onClick={() => handleSort('submissionDays')} style={{width: "5px", height: "10px", fontSize: "20px", display:"flex", justifyContent: "center", alignItems: "center"}}>↑↓</button></th>
          <th> Days Badge <button onClick={() => handleSort('daysBadgeCount')} style={{width: "5px", height: "10px", fontSize: "20px", display:"flex", justifyContent: "center", alignItems: "center"}}>↑↓</button></th>
          <th> Rating <button onClick={() => handleSort('rating')} style={{width: "5px", height: "10px", fontSize: "20px", display:"flex", justifyContent: "center", alignItems: "center"}}>↑↓</button></th>
          <th> Contest Badge <button onClick={() => handleSort('badge')} style={{width: "5px", height: "10px", fontSize: "20px", display:"flex", justifyContent: "center", alignItems: "center"}}>↑↓</button></th>
          <th> 
            Main Language 
            <button onClick={() => handleSort('primaryLanguage')} style={{width: "5px", height: "10px", fontSize: "20px", display:"flex", justifyContent: "center", alignItems: "center"}}>↑↓</button> 
            <button onClick={() => handleSort('primaryLanguageCount')} style={{width: "5px", height: "10px", fontSize: "20px", display:"flex", justifyContent: "center", alignItems: "center"}}>↑↓</button>
          </th>
          <th>Badges<button onClick={() => handleSort('badgeCount')} style={{width: "5px", height: "10px", fontSize: "20px", display:"flex", justifyContent: "center", alignItems: "center"}}>↑↓</button></th>
        </tr>
      </thead>
      <tbody>
        {sortedData.map((row, index) => (
          <tr key={row.ranking}>
            <td>{index + 1}</td>
            <td>{row.ranking}</td>
            <td>{<td><img style={{ width: 32, height: 24}} src={row.countryCodePNG} alt="" /></td>}{row.countryName}</td>
            <td>{<td><img style={{ width: 32, height: 32}} src={row.userAvatar} alt="" /></td>}<a href={`https://leetcode.com/u/${row.username}`} target="_blank" rel="noopener noreferrer">
  {row.realName}<br />{row.username}
</a><br />{row.school}<br />{row.company}</td>
            <td>{row.totalProblemsSolved}/<br />3586</td>
            <td>{row.easySolved}/<br />882</td>
            <td>{row.mediumSolved}/<br />1861</td>
            <td>{row.hardSolved}/<br />843</td>
            <td>{row.acceptanceRate}%</td>
            <td>{row.submissions}</td>
            <td>{row.currentStreak} Days<br /> <p style={{ fontSize: '11px' }}>{row.currentStreakDates[0]} <br />- {row.currentStreakDates[1]}</p> </td>
            <td>{row.maxStreak} Days<br /> <p style={{ fontSize: '11px' }}>{row.longestStreakDates[0]} <br />- {row.longestStreakDates[1]}</p> </td>
            <td>{row.submissionDays}<br /> <p style={{ fontSize: '10px' }}>{row.submissionsPerYear[0]}<br /> {row.submissionsPerYear[1]}<br /> {row.submissionsPerYear[2]}<br /> {row.submissionsPerYear[3]}<br /> {row.submissionsPerYear[4]}<br /> {row.submissionsPerYear[5]}<br /> {row.submissionsPerYear[6]}<br /> {row.submissionsPerYear[7]}<br /> {row.submissionsPerYear[8]}<br /> {row.submissionsPerYear[9]}<br /> {row.submissionsPerYear[10]}<br /> {row.submissionsPerYear[11]}<br /> {row.submissionsPerYear[12]}</p></td>
            <td>{<td><img style={{ width: 32, height: 32}} src={row.daysBadgeCount} alt="None" /></td>}</td>
            <td>{row.rating}</td>
            <td>{<td><img style={{ width: 32, height: 32}} src={row.badgePNG} alt="" /></td>}{row.badge}</td>
            <td>{<td><img style={{ width: 32, height: 32}} src={row.primaryLanguagePNG} alt="" /></td>} {row.primaryLanguage} <br /> {row.primaryLanguageCount}</td>
            <td>{row.badgeCount}<br /> <p style={{ fontSize: '10px' }}>{row.badgeCategories[0]}/1 Contest<br /> {row.badgeCategories[1]}/4 Submit<br /> {row.badgeCategories[2]}/11 Annual<br /> {row.badgeCategories[3]}/62 Daily<br /> {row.badgeCategories[4]}/38 Study</p></td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default SortableTable;
