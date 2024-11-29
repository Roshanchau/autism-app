import React from 'react';
import { View, TouchableOpacity, Text, StyleSheet , Image } from 'react-native';
import { useNavigation, NavigationProp } from '@react-navigation/native';
import RootStackParamList from './type'; 
import { Hero } from '@/assets/texts';

const hero = require('./home.png');
const school = require('./school.png');
const frequent = require('./frequent.png');
const free = require('./free.png');

const images=[hero,school, free ,frequent];

export default function HeroScreen() {
  const navigation = useNavigation<NavigationProp<RootStackParamList>>();

  const handleBoxPress = (boxNumber: string) => {
    if(boxNumber===Hero[0]){
      navigation.navigate('Home');
    }
    else if(boxNumber===Hero[1]){
      navigation.navigate('School');
    }
    else if(boxNumber===Hero[2]){
      navigation.navigate('free');
    }
    else if(boxNumber===Hero[3]){
      navigation.navigate('frequent');
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.boxContainer}>
      {Hero.map((item, index) => {
         const image = images.find((img, imgIndex) => imgIndex === index);
         return(

          <View key={index}>
            <TouchableOpacity
              style={[styles.box, { backgroundColor: '#FF6B6B' }]}
              onPress={() => handleBoxPress(item)}
            >
               <Image
                  source={image}
                  style={[styles.box]}
                />
            </TouchableOpacity>
            <Text style={styles.boxTextBelow}>{item}</Text>
          </View>
         )
})}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  boxContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    alignItems: 'center',
    width: 240, // Adjust width to fit two boxes per row
  },
  box: {
    width: 100,
    height: 100,
    justifyContent: 'center',
    alignItems: 'center',
    margin: 10,
  },
  boxText: {
    color: '#fff',
    fontSize: 18,
  },
  boxTextBelow: {
    color: '#000',
    fontSize: 18,
    marginTop: 5,
    textAlign: 'center',
    alignSelf: 'center',
  },
});