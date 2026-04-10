import React, { createContext, useState } from 'react';

export const ExamContext = createContext();

export const ExamProvider = ({ children }) => {
  const [selectedSection, setSelectedSection] = useState(null);
  const [selectedModule, setSelectedModule] = useState(null);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [selectedSubtopic, setSelectedSubtopic] = useState(null);

  const resetSelection = () => {
    setSelectedSection(null);
    setSelectedModule(null);
    setSelectedTopic(null);
    setSelectedSubtopic(null);
  };

  const value = {
    selectedSection,
    setSelectedSection,
    selectedModule,
    setSelectedModule,
    selectedTopic,
    setSelectedTopic,
    selectedSubtopic,
    setSelectedSubtopic,
    resetSelection,
  };

  return <ExamContext.Provider value={value}>{children}</ExamContext.Provider>;
};
