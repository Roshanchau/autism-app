import React, { useState, useEffect } from 'react';
import { Text, SafeAreaView, StyleSheet, FlatList, Button } from 'react-native';
import { Card } from 'react-native-paper';

export default function App() {
  const [displayList, setDisplayList] = useState([]);
  const [counter, setCounter] = useState(0); // Counter state

  const fetchDisplayWords = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/display_words?count=${counter}`); // Replace with your local IP
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setDisplayList(data);
    } catch (error) {
      console.error('Failed to fetch:', error);
    }
  };

  const handleRefresh = () => {
    if (counter >= 3) {
      setCounter(0); // Reset counter if it exceeds 3
    } else {
      setCounter(counter + 1); // Increment counter
    }
  };

  useEffect(() => {
    fetchDisplayWords(); // Fetch words on initial load
  }, [counter]); // Fetch words when counter changes

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.paragraph}>Refresh the list to see generated words!</Text>
      <Button title="Refresh List" onPress={handleRefresh} />
      <Card style={styles.card}>
        <FlatList
          data={displayList}
          renderItem={({ item }) => <Text style={styles.word}>{item}</Text>}
          keyExtractor={(item, index) => index.toString()}
        />
      </Card>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    backgroundColor: '#ecf0f1',
    padding: 8,
  },
  paragraph: {
    margin: 24,
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  card: {
    padding: 10,
  },
  word: {
    fontSize: 16,
    padding: 5,
    textAlign: 'center',
  },
});
