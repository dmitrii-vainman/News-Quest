import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';  // ✅ Add this import
import App from './App';

test('renders welcome message', () => {
    render(<App />);
    const linkElement = screen.getByText(/Willkommen zu meiner React-App/i);
    expect(linkElement).toBeInTheDocument();
});
