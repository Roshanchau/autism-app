import React, { useEffect, useState } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  TouchableOpacity, 
  TextInput, 
  FlatList,
  Modal,
  SafeAreaView,Alert
} from 'react-native';
import Icon from "react-native-vector-icons/MaterialIcons";
import * as Speech from "expo-speech";

interface Sentence {
  id: string;
  text: string;
  frequency: number;
}

export default function FrequentSentences() {
  const [modalVisible, setModalVisible] = useState(false);
  const [frequentSentence , setfrequentSentence]=useState([])

  useEffect(()=>{
    getSentences();
  },[])

  const getSentences = async () => {
    try {
      const response = await fetch(' http://192.168.1.66:5000/api/huu');
      const data = await response.json();
      console.log("API response:", data);
  
      // Ensure the data is in the expected format
      const transformedData = data.map((item: any , id:any) => {
        console.log("Item:", item);
        return {
          text: item,
          id:id
        };
      });
  
      setfrequentSentence(transformedData);
      console.log("Transformed data:", transformedData);
    } catch (err) {
      console.log(err);
    }
  };

  const speak = async (textToSpeak: string) => {
    try {
      await Speech.speak(textToSpeak);
    } catch (error) {
      console.error("Failed to speak:", error);
      Alert.alert("Error", "Failed to speak. Please try again.");
    }
  };

  const renderSentenceCard = ({ item }: { item: Sentence }) => (
    <TouchableOpacity style={styles.card} onPress={()=>speak(item.text)}>
      <Text style={styles.cardText}>{item.text}</Text>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Frequent Sentences</Text>
      <FlatList
        data={frequentSentence}
        renderItem={renderSentenceCard}
        keyExtractor={item => item.id}
        contentContainerStyle={styles.listContainer}
      />
      <TouchableOpacity 
        style={styles.addButton} 
        onPress={() => setModalVisible(true)}
      >
        <Icon name="add" size={30} color="white" />
      </TouchableOpacity>
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalView}>
          <Text style={styles.modalTitle}>Add New Sentence</Text>
          <TextInput
            style={styles.input}
            placeholder="Enter new sentence"
            multiline
          />
          <View style={styles.modalButtons}>
            <TouchableOpacity 
              style={[styles.button, styles.buttonClose]}
              onPress={() => setModalVisible(false)}
            >
              <Text style={styles.textStyle}>Cancel</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.button, styles.buttonSubmit]}
              onPress={() => setModalVisible(false)}
            >
              <Text style={styles.textStyle}>Add</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f0f0f0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    color: '#333',
  },
  listContainer: {
    paddingBottom: 100,
  },
  card: {
    backgroundColor: 'white',
    borderRadius: 10,
    padding: 20,
    marginBottom: 15,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  cardText: {
    fontSize: 18,
    marginBottom: 10,
    color: '#333',
  },
  frequencyText: {
    fontSize: 14,
    color: '#888',
  },
  addButton: {
    position: 'absolute',
    right: 30,
    bottom: 30,
    backgroundColor: '#007AFF',
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 3,
  },
  modalView: {
    margin: 20,
    marginTop: 100,
    backgroundColor: "white",
    borderRadius: 20,
    padding: 35,
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 2
    },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  input: {
    height: 100,
    width: '100%',
    marginBottom: 15,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 5,
    padding: 10,
    textAlignVertical: 'top',
  },
  modalButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '100%',
  },
  button: {
    borderRadius: 20,
    padding: 10,
    elevation: 2,
    width: '45%',
  },
  buttonClose: {
    backgroundColor: "#FF6B6B",
  },
  buttonSubmit: {
    backgroundColor: "#4CAF50",
  },
  textStyle: {
    color: "white",
    fontWeight: "bold",
    textAlign: "center"
  },
});