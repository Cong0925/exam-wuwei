import React, { useState, useEffect } from 'react';

// 定义组件的 Props 类型
interface Props {
  userId: string; // 用户 ID
}

// 定义 UserData 组件
const UserData: React.FC<Props> = ({ userId }) => {
  // 定义状态
  const [user, setUser] = useState<any>(null); // 存储用户数据
  const [seconds, setSeconds] = useState<number>(0); // 计时器状态
  let intervalId: number | NodeJS.Timeout; // 定时器 ID

  // 获取用户数据的函数
  const fetchUserData = () => {
    // 发起 API 请求获取用户数据
    fetch(`https://secret.url/user/${userId}`)
      .then(response => {
        // 检查响应状态
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => setUser(data)) // 更新用户数据状态
      .catch(error => console.error('Error fetching user data:', error)); // 错误处理
  };

  // useEffect 用于处理副作用
  useEffect(() => {
    // 调用函数获取用户数据
    fetchUserData();
    
    // 启动定时器，每秒更新计时器状态
    intervalId = setInterval(() => {
      setSeconds(prevSeconds => prevSeconds + 1);
    }, 1000);

    // 清理副作用：组件卸载时清除定时器
    return () => {
      clearInterval(intervalId);
    };
  }, [userId]); // 依赖项是 userId，当 userId 变化时重新执行

  useEffect(() => {
    // 只在组件卸载时执行清理
    return () => {
      clearInterval(intervalId); // 确保在组件卸载时清除定时器
    };
  }, []); // 空依赖数组，确保仅在组件卸载时执行

  useEffect(() => {
    if (user) {
      // 用户数据加载完成时输出日志
      console.log('User data loaded:', user);
    }
  }, [user]); // 依赖项是 user，当 user 数据变化时执行

  return (
    <div>
      <h1>User Data Component</h1>
      {user ? (
        <div>
          <p>Name: {user.name}</p>
          <p>Email: {user.email}</p>
        </div>
      ) : (
        <p>Loading user data...</p>
      )}
      <p>Timer: {seconds} seconds</p>
    </div>
  );
};

export default UserData;



