import styled from "styled-components";

export const StateContent = styled.div`
  fill: #632956;
  stroke: white;
  stroke-width: 1px;

  svg {
    width: 450px;
    height: 450px;
  }
`;

interface TooltipProps {
  display?: string
  position: { top?: number, left?: number };
};

export const Tooltip = styled.div<TooltipProps>`
  position: absolute;
  display: ${props => props.display || "none"};
  top: ${props => `${props.position.top}px` || "0px"};
  left: ${props => `${props.position.left}px` || "0px"};
`;

export const TooltipContent = styled.div`
  background-color: #34679A;
  
  padding: 3px 8px;
  border-radius: 5px;
  
  font-size: 10px;
  color: white;
  font-weight: 400;
`;