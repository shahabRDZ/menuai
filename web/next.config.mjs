/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    serverActions: {
      bodySizeLimit: "12mb",
      allowedOrigins: [
        "localhost:3000",
        "127.0.0.1:3000",
        "0.0.0.0:3000",
        "192.168.1.105:3000",
      ],
    },
  },
};

export default nextConfig;
