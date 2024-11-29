import React from 'react';
import { NavigationContainer , NavigationIndependentTree } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import HeroScreen from './HomeScreen';
import Screen1 from '../../screens/Screen1';
import Screen2 from '../../screens/Screen2';
import Screen3 from '@/screens/Screen3';
import Screen4 from '../../screens/Screen4';
import './global.css';

import  RootStackParamList  from './type';

const Stack = createStackNavigator<RootStackParamList>();

export default function App() {
  return (
    <NavigationIndependentTree>
    <NavigationContainer >
      <Stack.Navigator initialRouteName="HeroScreen">
        <Stack.Screen name="HeroScreen"
          options={{ headerShown: false }} 
        component={HeroScreen} />
        <Stack.Screen name="Home" component={Screen1} />
        <Stack.Screen name="School" component={Screen2} />
        <Stack.Screen name="free" component={Screen3} />
        <Stack.Screen name="frequent" component={Screen4} />
      </Stack.Navigator>
    </NavigationContainer>
    </NavigationIndependentTree>
  );
}