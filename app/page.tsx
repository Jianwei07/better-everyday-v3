"use client";

import dynamic from "next/dynamic";

const Chatbot = dynamic(() => import("./components/Chatbot"), {
  ssr: false,
});

const HomePage = () => {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-8">
        Welcome to My Personal Website
      </h1>
      <Chatbot />
    </div>
  );
};

export default HomePage;
