'use client'

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUserNurse, faUserDoctor, faUser } from '@fortawesome/free-solid-svg-icons';

import { AtendimentosContent, AtendimentosSection, BigNumber, FourGrid, Number } from "./styles";


const Atendimentos = () => {
  const Data = [
    {
      id: 1,
      year: 2016,
      userGain: 80000,
      userLost: 823
    },
    {
      id: 2,
      year: 2017,
      userGain: 45677,
      userLost: 345
    },
    {
      id: 3,
      year: 2018,
      userGain: 78888,
      userLost: 555
    },
    {
      id: 4,
      year: 2019,
      userGain: 90000,
      userLost: 4555
    },
    {
      id: 5,
      year: 2020,
      userGain: 4300,
      userLost: 234
    }
  ];

  const data = {
    labels: ['Red', 'Orange', 'Blue'],
    // datasets is an array of objects where each object represents a set of data to display corresponding to the labels above. for brevity, we'll keep it at one object
    datasets: [
      {
        label: 'Popularity of colours',
        data: [55, 23, 96],
        // you can set indiviual colors for each bar
        backgroundColor: [
          'rgba(255, 255, 255, 0.6)',
          'rgba(255, 255, 255, 0.6)',
          'rgba(255, 255, 255, 0.6)'
        ],
        borderWidth: 1,
      }
    ]
  }

  return (
    <AtendimentosSection>
      <h1>Atendimentos</h1>
      <AtendimentosContent>
        <div>
          <FourGrid>
            <div>
              <BigNumber>
                <h2>43021</h2>
              </BigNumber>
              <p>Número de atendimentos individuais já registrados</p>
            </div>
            <div>
              <BigNumber>
                <h2>4</h2>
                <h3>atendimentos por pessoa</h3>
              </BigNumber>
              <p>Atendimento por população total ao decorrer dos anos já registrados</p>
            </div>
          </FourGrid>
        </div>
        <div>
          <FourGrid>
            <div>
              <BigNumber>
                <FontAwesomeIcon icon={faUserDoctor} size="3x" color="#343A40" />
                <Number>
                  <h2>4</h2>
                  <h3>atendimentos por pessoa</h3>
                </Number>
              </BigNumber>
            </div>
            <div>
              <BigNumber>
                <FontAwesomeIcon icon={faUserNurse} size="3x" color="#343A40" />
                <Number>
                  <h2>4</h2>
                  <h3>atendimentos por pessoa</h3>
                </Number>
              </BigNumber>
            </div>
            <div>
              <BigNumber>
                <FontAwesomeIcon icon={faUser} size="3x" color="#343A40" />
                <Number>
                  <h2>4</h2>
                  <h3>atendimentos por pessoa</h3>
                </Number>
              </BigNumber>
            </div>
          </FourGrid>
        </div>
      </AtendimentosContent>
    </AtendimentosSection>
  )
}

export default Atendimentos;