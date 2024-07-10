/** @type {import('next').NextConfig} */
const nextConfig = {
    async redirects() {
        return [
          {
            source: '/ask',
            destination: 'http://localhost:5000/ask', // Your assistant server endpoint
            permanent: false, // Set to true for production
          },
        ];
      },
};



export default nextConfig;
