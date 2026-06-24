"use client";

import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { Thermometer, Droplets, Sun, Activity, Lightbulb } from "lucide-react";

interface SensorData {
  id: number;
  time: string;
  temp: number;
  hum: number;
  light: number;
  mode: string;
}

export default function Dashboard() {
  const [data, setData] = useState<SensorData[]>([]);
  const [status, setStatus] = useState({ system_report: "Đang tải báo cáo...", ai_advice: "Đang kết nối AI ..." }); 
  const [loading, setLoading] = useState(true);
  

  const API_BASE = "http://192.168.19.116:8000";

  useEffect(() => {
    // Hàm lấy dữ liệu cảm biến
    // const fetchData = async () => {
    //   try {
    //     const response = await fetch(`${API_BASE}/data`);
    //     const result = await response.json();
    //     setData(result.reverse());
    //     setLoading(false);
    //   } catch (error) {
    //     console.error("Lỗi fetch dữ liệu cảm biến:", error);
    //   }
    // };

    const fetchData = async () => {
      try {
        const response = await fetch(`${API_BASE}/data`);
        const result = await response.json();
        
        // Kỹ thuật phòng thủ: Chỉ set data nếu result thực sự là một mảng
        if (Array.isArray(result)) {
            setData(result.reverse());
        } else {
            console.error("Dữ liệu trả về không hợp lệ (Không phải Array):", result);
            // Có thể thêm setState để hiển thị lỗi ra UI cho người dùng biết
        }
        setLoading(false);
      } catch (error) {
        console.error("Lỗi fetch dữ liệu cảm biến:", error);
        setLoading(false);
      }
    };

    // Hàm lấy lời khuyên từ AI
    // const fetchAdvice = async () => {
    //   try {
    //     const res = await fetch(`${API_BASE}/advice`);
    //     const data = await res.json();
    //     setAdvice(data.advice);
    //   } catch (err) {
    //     setAdvice("Chưa kết nối được với AI.");
    //   }
    // };
    // Trong useEffect
    const fetchStatus = async () => {
      try {
        const res = await fetch(`${API_BASE}/status`);
        const result = await res.json();
        setStatus(result);
      } catch (err) {
        setStatus({ system_report: "Lỗi kết nối", ai_advice: "Lỗi kết nối" });
      }
    };

    // Gọi nó
    fetchStatus();
    const dataInterval = setInterval(fetchData, 5000);
    const statusInterval = setInterval(fetchStatus, 2000); // Check nhanh hơn nếu muốn
    // Đừng quên thêm statusInterval vào phần clearInterval ở return nhé
        fetchData();
        //fetchAdvice();

    // Tự động cập nhật mỗi 5 giây (cảm biến) và 60 giây (AI)
    const interval = setInterval(() => {
      fetchData();
    }, 5000);
    
    // const adviceInterval = setInterval(fetchAdvice, 60000);

    return () => {
      clearInterval(interval);
      clearInterval(dataInterval);
      clearInterval(statusInterval);
      //clearInterval(adviceInterval);
    };
  }, []);

  if (loading) return <div className="p-10 text-center text-xl">Đang tải dữ liệu nhà kính...</div>;

  return (
    <main className="p-4 md:p-8 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">🌱 Miniature Greenhouse Dashboard</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Biểu đồ */}
        {/* Sửa lại đoạn Biểu đồ này trong page.tsx */}
        <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100" style={{ minHeight: '300px' }}>
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2 text-gray-700">
            <Activity className="text-purple-500" /> Biểu đồ theo dõi
          </h2>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" hide />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="temp" stroke="#ef4444" name="Nhiệt độ (°C)" strokeWidth={2} />
                <Line type="monotone" dataKey="hum" stroke="#3b82f6" name="Độ ẩm (%)" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Trạng thái hiện tại */}
        <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2 text-gray-700">
            <Sun className="text-yellow-500" /> Thông số thời gian thực
          </h2>
          {data.length > 0 ? (
            <div className="space-y-6">
              <div className="flex justify-between items-center p-4 bg-red-50 rounded-lg">
                <span className="font-medium text-red-600">Nhiệt độ:</span>
                <span className="text-2xl font-bold">{data[data.length - 1].temp}°C</span>
              </div>
              <div className="flex justify-between items-center p-4 bg-blue-50 rounded-lg">
                <span className="font-medium text-blue-600">Độ ẩm:</span>
                <span className="text-2xl font-bold">{data[data.length - 1].hum}%</span>
              </div>
              <div className="text-sm text-gray-500 italic">
                Thời gian: {data[data.length - 1].time} | Chế độ: {data[data.length - 1].mode}
              </div>
            </div>
          ) : (
            <p>Chưa có dữ liệu</p>
          )}
        </div>
      </div>

      

    {/* 2 Khối tách biệt: Hệ thống & AI */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
        
        {/* Phần 1: Báo cáo hệ thống (Tức thì) */}
        <div className="bg-white p-6 rounded-xl shadow-lg border-l-4 border-emerald-500">
          <h2 className="text-xl font-semibold text-slate-800 mb-2">Báo cáo Hệ thống</h2>
          <p className="text-slate-700 leading-relaxed italic">{status.system_report}</p>
          <div className="mt-4 text-xs text-slate-400">
          Hệ thống phân tích tự động - Cập nhật lúc {new Date().toLocaleTimeString()}
          </div>
        </div>

        {/* Phần 2: AI Consultant (Phân tích) */}
        <div className="bg-white p-6 rounded-xl shadow-lg border-l-4 border-indigo-500">
          <h2 className="text-xl font-semibold text-slate-800 mb-2">Góc nhìn chuyên gia (Gemini AI)</h2>
          <p className="text-slate-700 leading-relaxed">{status.ai_advice}</p>
        </div>

      </div>
    </main>
  );
}