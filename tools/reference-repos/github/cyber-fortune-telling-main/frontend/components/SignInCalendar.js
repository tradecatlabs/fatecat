import React, { useState, useEffect } from 'react';
import { Box, Button, Card, Typography, IconButton, Fade, CircularProgress } from '@mui/material';
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';
import CloseIcon from '@mui/icons-material/Close';
import axios from 'axios';
import moment from 'moment';

// API 配置
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:11337";
const API_TOKEN = process.env.NEXT_PUBLIC_API_TOKEN || "";

// Helper to get all days in current month
function getMonthDays(year, month) {
  const days = [];
  const date = new Date(year, month, 1);
  while (date.getMonth() === month) {
    days.push(new Date(date));
    date.setDate(date.getDate() + 1);
  }
  return days;
}

export default function SignInCalendar({ fortune_telling_uid }) {
  const [open, setOpen] = useState(false);
  const [signInDays, setSignInDays] = useState([]); // Array of YYYY-MM-DD
  const [loading, setLoading] = useState(false);
  const [signingIn, setSigningIn] = useState(false);
  const [error, setError] = useState(null);
  const today = moment().format('YYYY-MM-DD');
  const currentYear = moment().year();
  const currentMonth = moment().month();
  const [viewYear, setViewYear] = useState(currentYear);
  const [viewMonth, setViewMonth] = useState(currentMonth);
  const days = getMonthDays(viewYear, viewMonth);

  const handlePrevMonth = () => {
    if (viewMonth === 0) {
      setViewYear(viewYear - 1);
      setViewMonth(11);
    } else {
      setViewMonth(viewMonth - 1);
    }
  };
  const handleNextMonth = () => {
    if (viewMonth === 11) {
      setViewYear(viewYear + 1);
      setViewMonth(0);
    } else {
      setViewMonth(viewMonth + 1);
    }
  };

  // Fetch sign-in data
  useEffect(() => {
    if (!open) return;
    setLoading(true);
    setError(null);
    axios.get(`${API_BASE_URL}/api/sign-in/dates`, {
      headers: { Authorization: API_TOKEN ? `Bearer ${API_TOKEN}` : undefined },
      params: { sign_in_uid: fortune_telling_uid, year: viewYear, month: viewMonth + 1 }
    })
      .then(res => {
        // res.data.sign_in_date_list is an array of YYYY-MM-DD
        setSignInDays(res.data.sign_in_date_list || []);
      })
      .catch(() => setError('获取签到信息失败'))
      .finally(() => setLoading(false));
  }, [open, fortune_telling_uid, viewYear, viewMonth]);

  // Handle sign-in
  const handleSignIn = async () => {
    setSigningIn(true);
    setError(null);
    try {
      await axios.post(`${API_BASE_URL}/api/sign-in`, {
        sign_in_uid: fortune_telling_uid,
        sign_in_date: today
      }, {
        headers: { Authorization: API_TOKEN ? `Bearer ${API_TOKEN}` : undefined }
      });
      setSignInDays(prev => [...prev, today]);
    } catch (e) {
      setError('签到失败');
    } finally {
      setSigningIn(false);
    }
  };

  // UI
  return (
    <>
      {!open && (
        <Box sx={{ position: 'fixed', top: 80, right: 20, zIndex: 2000 }}>
          <IconButton
            color="primary"
            sx={{ background: '#FFD700', boxShadow: 3, '&:hover': { background: '#F4C430' } }}
            onClick={() => setOpen(true)}
            size="large"
          >
            <CalendarMonthIcon sx={{ fontSize: 36, color: '#1A237E' }} />
          </IconButton>
        </Box>
      )}
      {open && (
        <Fade in={open} unmountOnExit>
          <Box sx={{ position: 'fixed', top: 80, right: 20, zIndex: 2000, minWidth: 320, minHeight: 370, display: 'flex', alignItems: 'flex-end', justifyContent: 'flex-end' }}>
            <Card sx={{ minWidth: 320, p: 2, position: 'relative', boxShadow: 6, border: '2px solid #FFD700', background: 'rgba(255,255,255,0.98)' }}>
              <IconButton size="small" sx={{ position: 'absolute', top: 8, right: 8 }} onClick={() => setOpen(false)}>
                <CloseIcon />
              </IconButton>
              <Typography variant="h6" sx={{ color: '#1A237E', fontWeight: 700, mb: 1 }}>每日签到</Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 1 }}>
                <Button size="small" onClick={handlePrevMonth} sx={{ minWidth: 0, px: 1 }}>&lt;</Button>
                <Typography variant="subtitle1" sx={{ mx: 2, fontWeight: 600 }}>
                  {viewYear}年{viewMonth + 1}月
                </Typography>
                <Button size="small" onClick={handleNextMonth} sx={{ minWidth: 0, px: 1 }}>&gt;</Button>
              </Box>
              <Box sx={{ minHeight: 270, display: 'flex', flexDirection: 'column', justifyContent: 'flex-start', mb: 1 }}>
                <Typography variant="body2" sx={{ color: '#1A237E', fontWeight: 500, textAlign: 'center', mb: 1 }}>
                  累计签到：{signInDays.length} 天
                </Typography>
                {loading ? (
                  <Box sx={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <CircularProgress />
                  </Box>
                ) : (
                  <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: 0.5, flex: 1 }}>
                    {[...Array(new Date(viewYear, viewMonth, 1).getDay()).keys()].map(i => <Box key={i} />)}
                    {days.map(day => {
                      const d = moment(day).format('YYYY-MM-DD');
                      const signed = signInDays.includes(d);
                      const isToday = d === today;
                      return (
                        <Box
                          key={d}
                          sx={{
                            width: 36, height: 36, display: 'flex', alignItems: 'center', justifyContent: 'center',
                            borderRadius: '50%',
                            background: signed ? (isToday ? '#FFD700' : '#F4C430') : (isToday ? '#FFF8DC' : 'transparent'),
                            color: signed ? '#1A237E' : (isToday ? '#FFD700' : '#1A237E'),
                            fontWeight: isToday ? 700 : 400,
                            border: isToday ? '2px solid #FFD700' : 'none',
                            boxShadow: signed ? 2 : 0,
                          }}
                        >
                          {day.getDate()}
                        </Box>
                      );
                    })}
                  </Box>
                )}
              </Box>
              <Button
                variant="contained"
                fullWidth
                sx={{ background: '#FFD700', color: '#1A237E', fontWeight: 700, mt: 1, mb: 1, '&:hover': { background: '#F4C430' } }}
                disabled={signInDays.includes(today) || signingIn || !(viewYear === currentYear && viewMonth === currentMonth)}
                onClick={handleSignIn}
              >
                {signingIn ? '签到中...' : signInDays.includes(today) ? '今日已签到' : (viewYear === currentYear && viewMonth === currentMonth ? '一键签到' : '只能在当月签到')}
              </Button>
              {error && <Typography color="error" variant="body2">{error}</Typography>}
            </Card>
          </Box>
        </Fade>
      )}
    </>
  );
} 