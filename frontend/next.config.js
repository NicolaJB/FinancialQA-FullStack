// frontend/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,  // React strict mode enabled
  swcMinify: true,        // SWC minification enabled for production builds

  // Environment variables exposed to the frontend
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
  },
};

module.exports = nextConfig;
