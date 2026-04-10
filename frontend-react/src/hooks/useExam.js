import { useContext } from 'react';
import { ExamContext } from '../context/ExamContext';

export const useExam = () => {
  const context = useContext(ExamContext);
  if (!context) {
    throw new Error('useExam must be used within ExamProvider');
  }
  return context;
};
